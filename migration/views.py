import copy
import json
from datetime import datetime
from os import remove
from logging import log

import pandas as pd
import requests
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from company_migration.settings import BASE_DIR
from helpers.authenticate import re_auth, get_api_key
from helpers.cities_and_branches import CitiesAndBranches
from helpers.modify_auth_json import ModifyAuthJson
from helpers.publish_all_processes import UpdateProcessMaster
from helpers.utils import env_variables_to_dataframe, download_file
from helpers.datastore import DatastoreMigration

temp_files_path = BASE_DIR + '/temp_files/'


class MigrateEnvVariables(generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        file_path = temp_files_path + 'env_variables_' + datetime.now().strftime("%d%m%Y_%H%M%S") + '.xls'
        re_auth('source')
        re_auth('target')
        auth_json = ModifyAuthJson()

        env_variables = pd.DataFrame({'key': [], 'value': [], 'language': [], 'Type': []})
        params = {
            'page': 0,
            'size': 5000,
            'sortOn': 'id',
            'sortType': 'ASC',
            'type': 'SYSTEM'
        }
        response = requests.get(auth_json.get_base_url('source') + 'v1/app/rest/getAllVariablesV2',
                                params=params,
                                cookies=auth_json.get_cookies('source'))
        if response.status_code != 200:
            return Response({
                'success': False,
                'data': {
                    'request': 'get SYSTEM env variables',
                    'server': auth_json.get_base_url('source'),
                    'body': json.loads(response.content),
                    'status': response.status_code
                }
            }, status=response.status_code)
        system_variables = json.loads(response.content)
        env_variables = pd.concat([env_variables, env_variables_to_dataframe(system_variables['content'])])
        params['type'] = 'LANGUAGE'
        response = requests.get(auth_json.get_base_url('source') + 'v1/app/rest/getAllVariablesV2',
                                params=params,
                                cookies=auth_json.get_cookies('source'))
        if response.status_code != 200:
            return Response({
                'success': False,
                'data': {
                    'request': 'get LANGUAGE env variables',
                    'server': auth_json.get_base_url('source'),
                    'body': json.loads(response.content),
                    'status': response.status_code
                }
            }, status=response.status_code)
        language_variables = json.loads(response.content)
        env_variables = pd.concat([env_variables, env_variables_to_dataframe(language_variables['content'])])
        env_variables.to_excel(file_path, index=False)

        file = {'file': ('env_variables.xls', open(file_path, 'rb'), 'application/vnd.ms-excel')}

        response = requests.post(
            auth_json.get_base_url('target') + 'v1/app/rest/upload_variable_data',
            headers=auth_json.get_xsrf_header('target'),
            cookies=auth_json.get_cookies('target'),
            files=file
        )
        if response.status_code != 200:
            return Response({
                'success': False,
                'data': {
                    'request': 'upload env variables excel',
                    'server': auth_json.get_base_url('target'),
                    'body': json.loads(response.content),
                    'status': response.status_code
                }
            }, status=response.status_code)
        remove(file_path)
        return Response({
            'success': True,
            'message': 'Environment variables migrated successfully'
        }, status=status.HTTP_200_OK)


class MigrateCompanySettings(generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        file_path = temp_files_path + 'company_settings' + datetime.now().strftime("%d%m%Y_%H%M%S") + '.json'
        re_auth('source')
        re_auth('target')
        auth_json = ModifyAuthJson()

        response = requests.get(
            url=auth_json.get_base_url('source') + "v1/app/rest/download_company_json_configuration",
            cookies=auth_json.get_cookies('source')
        )
        if response.status_code != 200:
            return Response({
                'success': False,
                'data': {
                    'request': 'download company settings',
                    'server': auth_json.get_base_url('source'),
                    'body': json.loads(response.content),
                    'status': response.status_code
                }
            }, status=response.status_code)
        with open(file_path, "wb") as outfile:
            outfile.write(response.content)
            outfile.close()

        file = {'file': ('company_settings.json', open(file_path, 'rb'), 'application/json')}
        response = requests.post(auth_json.get_base_url('target') + "v1/app/rest/user_mapping_json_upload",
                                 cookies=auth_json.get_cookies('target'),
                                 headers=auth_json.get_xsrf_header('target'),
                                 files=file)
        if response.status_code != 200:
            return Response({
                'success': False,
                'data': {
                    'request': 'upload company settings',
                    'server': auth_json.get_base_url('target'),
                    'body': json.loads(response.content),
                    'status': response.status_code
                }
            }, status=response.status_code)

        response_body = json.loads(response.content)
        fields = {
            'file': ('company_settings.json', open(file_path, 'rb'), 'application/json'),
            'userType': (None, json.dumps({
                'newUserTypes': response_body['newUserTypes'],
                'newToOldIdMap': response_body['newToOldIdMap']
            }))
        }
        response = requests.post(
            auth_json.get_base_url('target') + "v1/app/rest/upload_company_json",
            files=fields,
            cookies=auth_json.get_cookies('target'),
            headers=auth_json.get_xsrf_header('target'),
        )

        if response.status_code != 200:
            return Response({
                'success': False,
                'data': {
                    'request': 'upload company settings',
                    'server': auth_json.get_base_url('target'),
                    'body': json.loads(response.content),
                    'status': response.status_code
                }
            }, status=response.status_code)

        re_auth('target')
        remove(file_path)

        return Response({
            'success': True,
            'data': {
                'message': 'all company settings migrated successfully',
                'status': 'success'
            }
        }, status=status.HTTP_200_OK)


class PublishProcesses(generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        update_process_master = UpdateProcessMaster()
        update_process_master.get_process_config()
        update_process_master.get_process_versions()
        update_process_master.publish_processes()
        return Response({
            'success': True,
            'data': {
                'message': 'all process masters published successfully',
                'status': 'success'
            }
        }, status=status.HTTP_200_OK)


class MigrateCitiesAndBranches(generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        auth_json = ModifyAuthJson()
        source_headers = copy.deepcopy(auth_json.get_xsrf_header('source'))
        target_headers = copy.deepcopy(auth_json.get_xsrf_header('target'))
        target_headers['Content-Type'] = "application/json"

        cities_branches_obj = CitiesAndBranches(
            source_base_url=auth_json.get_base_url('source'),
            source_cookies=auth_json.get_cookies('source'),
            source_headers=source_headers,
            target_base_url=auth_json.get_base_url('source'),
            target_cookies=auth_json.get_cookies('target'),
            target_headers=target_headers
        )

        return Response({
            'success': True,
            'data': {
                'message': 'all cities and branches migrated successfully',
            }
        }, status=status.HTTP_200_OK)


class UpdatePostUrl(generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        re_auth('source')
        re_auth('target')
        auth_json = ModifyAuthJson()
        target_headers = copy.deepcopy(auth_json.get_xsrf_header('target'))
        target_headers['Content-Type'] = "application/json"

        api_key = get_api_key(
            base_url=auth_json.get_base_url('target'),
            cookies=auth_json.get_cookies('target'),
            headers=target_headers
        )

        response = requests.get(
            auth_json.get_base_url('target') + 'app/rest/get_connector_environment/send_updates',
            cookies=auth_json.get_cookies('target'))

        if response.status_code != 200:
            return Response({
                'success': False,
                'data': {
                    'request': 'get connector master settings',
                    'server': auth_json.get_base_url('target'),
                    'body': json.loads(response.content),
                    'status': response.status_code
                }
            }, status=response.status_code)
        connector_master_settings = json.loads(response.content)
        post_hook_url = str(connector_master_settings['postHookUrl'])
        api_key_old = post_hook_url.split('=')[1]
        connector_master_settings['postHookUrl'] = post_hook_url.replace(api_key_old, api_key)

        response = requests.post(
            auth_json.get_base_url('target') + 'app/rest/update_connector_master',
            data=json.dumps(connector_master_settings),
            cookies=auth_json.get_cookies('target'),
            headers=target_headers
        )

        if response.status_code != 200:
            return Response({
                'success': False,
                'data': {
                    'request': 'get connector master settings',
                    'server': auth_json.get_base_url('target'),
                    'body': json.loads(response.content),
                    'status': response.status_code
                }
            }, status=response.status_code)

        return Response({
            'success': True,
            'message': 'post hook url updated successfully'
        }, status=response.status_code)


class AddDefaultHub(generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        re_auth('target')
        auth_json = ModifyAuthJson()
        target_headers = auth_json.get_xsrf_header('target')
        target_headers['Content-Type'] = "application/json"
        response = requests.post(
            auth_json.get_base_url('target') + 'v1/app/rest/cities',
            data=json.dumps({
                'name': 'Default City',
                'enabled': True
            }),
            headers=target_headers,
            cookies=auth_json.get_cookies('target')
        )

        city_id = ''

        if response.status_code != 200:
            if 'City name already exist' not in str(response.content):
                return Response({
                    'success': False,
                    'data': {
                        'request': 'add default city',
                        'server': auth_json.get_base_url('target'),
                        'body': json.loads(response.content),
                        'status': response.status_code
                    }
                }, status=response.status_code)
            else:
                response = requests.get(
                    url=auth_json.get_base_url('target') + "v1/app/rest/cities",
                    cookies=auth_json.get_cookies('target')
                )
                if response.status_code != 200:
                    return Response({
                        'success': False,
                        'data': {
                            'request': 'get cities',
                            'server': auth_json.get_base_url('target'),
                            'body': json.loads(response.content),
                            'status': response.status_code
                        }
                    }, status=response.status_code)
                cities = json.loads(response.content)
                if 'Default City' in [city['name'] for city in cities]:
                    city_id = [city['id'] for city in cities if city['name'] == 'Default City'][0]
        else:
            city_id = (json.loads(response.content))['id']

        response = requests.get(
            url=auth_json.get_base_url('target') + 'v1/app/rest/hubs/pageable',
            cookies=auth_json.get_cookies('target'),
            params={
                'city_id': city_id,
                'pageNo': '0',
                'recordsPerPage': '500',
                'sortOn': 'id',
                'sortType': 'DESC'
            },
            headers=target_headers
        )

        should_add_branch = False
        branch_id = ''
        if response.status_code != 200 and response.status_code != 204:
            return Response({
                'success': False,
                'data': {
                    'request': 'get branch of Default City',
                    'server': auth_json.get_base_url('target'),
                    'body': json.loads(response.content),
                    'status': response.status_code
                }
            }, status=response.status_code)

        elif response.status_code == 204:
            should_add_branch = True
        elif response.status_code == 200:
            branches = json.loads(response.content)['content']
            if 'DefaultBranch' not in [branch['code'] for branch in branches]:
                should_add_branch = True
            else:
                branch_id = [branch['id'] for branch in branches if branch['code'] == 'DefaultBranch'][0]

        if should_add_branch:
            response = requests.post(
                auth_json.get_base_url('target') + 'v1/app/rest/hubs',
                data=json.dumps(
                    {
                        "defaultNewUI": False,
                        "name": "Default Branch",
                        "code": "DefaultBranch",
                        "enabled": True,
                        "timeZone": None,
                        "latitude": "0",
                        "longitude": "0",
                        "cityId": city_id
                    }),
                headers=target_headers,
                cookies=auth_json.get_cookies('target')
            )
            if response.status_code != 200:
                return Response({
                    'success': False,
                    'data': {
                        'request': 'add branch',
                        'server': auth_json.get_base_url('target'),
                        'body': json.loads(response.content),
                        'status': response.status_code
                    }
                }, status=response.status_code)
            branch_id = json.loads(response.content)['id']

        response = requests.get(
            auth_json.get_base_url('target') + 'v1/app/rest/users',
            params={
                'activatedUser': True,
                'pageNo': 0,
                'query': '',
                'recordsPerPage': 10,
                'sortOn': 'id',
                'sortType': 'ASC',
                'userTypeId': 1
            },
            cookies=auth_json.get_cookies('target')
        )

        if response.status_code != 200:
            return Response({
                'success': False,
                'data': {
                    'request': 'get admin users',
                    'server': auth_json.get_base_url('target'),
                    'body': json.loads(response.content),
                    'status': response.status_code
                }
            }, status=response.status_code)

        response_body = json.loads(response.content)
        admin_user = [user for user in response_body['content'] if user['login'] == auth_json.get_username('target')][0]

        payload = {
            'data': (None, json.dumps(
                {
                    "id": admin_user['id'],
                    "authUserId": None,
                    "login": admin_user['login'],
                    "firstName": admin_user['firstName'],
                    "lastName": admin_user['lastName'],
                    "email": admin_user['email'],
                    "mobileNumber": admin_user['mobileNumber'],
                    "employeeCode": admin_user['employeeCode'],
                    "userTypeId": 1,
                    "cityId": city_id,
                    "hubId": branch_id,
                    "activated": True,
                    "autoPushMailActivated": admin_user['autoPushMailActivated'],
                    "serviceProviderCode": admin_user['serviceProviderCode'],
                    "profileImage": admin_user['profileImage'],
                    "routingJson": admin_user['routingJson'],
                    "icdr": admin_user['icdr']
                }
            )),
            'companyId': (None, auth_json.get_company_id('target'))
        }
        del target_headers['Content-Type']
        response = requests.post(
            auth_json.get_base_url('target') + 'v1/app/rest/users/',
            cookies=auth_json.get_cookies('target'),
            headers=target_headers,
            files=payload
        )

        if response.status_code != 200:
            return Response({
                'success': False,
                'data': {
                    'request': 'assign city and branch to user',
                    'server': auth_json.get_base_url('target'),
                    'body': json.loads(response.content),
                    'status': response.status_code
                }
            }, status=response.status_code)

        return Response({
            'success': True,
            'message': 'city assigned to admin successfully'
        }, status=status.HTTP_200_OK)


class MigrateDataStore(generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        re_auth('source')
        re_auth('target')
        auth_json = ModifyAuthJson()

        datastore = DatastoreMigration()
        source_datastores = datastore.get_existing_datastores(
            base_url=auth_json.get_base_url('source'),
            headers=auth_json.get_xsrf_header('source'),
            cookies=auth_json.get_cookies('source')
        )

        target_datastores = datastore.get_existing_datastores(
            base_url=auth_json.get_base_url('target'),
            headers=auth_json.get_xsrf_header('target'),
            cookies=auth_json.get_cookies('target')
        )

        for source_datastore in source_datastores:
            re_auth('source')
            re_auth('target')
            datastore_attributes = datastore.get_datastore_attributes(
                base_url=auth_json.get_base_url('source'),
                headers=auth_json.get_xsrf_header('source'),
                cookies=auth_json.get_cookies('source'),
                dsm_id=source_datastore['id']
            )

            datastore.generate_datastore_dump_report(
                base_url=auth_json.get_base_url('source'),
                headers=auth_json.get_xsrf_header('source'),
                cookies=auth_json.get_cookies('source'),
                dsm_id=source_datastore['id'],
                ds_attributes=[ds_attribute['key'] for ds_attribute in datastore_attributes]
            )

            download_url = datastore.get_datastore_dump_download_url(
                base_url=auth_json.get_base_url('source'),
                headers=auth_json.get_xsrf_header('source'),
                cookies=auth_json.get_cookies('source'),
                dsm_id=source_datastore['id']
            )

            if download_url:
                csv_path = download_file(download_url)
                excel_path = datastore.convert_dump_to_excel(csv_path, datastore_attributes)
                remove(csv_path)
                datastore.upload_excel(
                    base_url=auth_json.get_base_url('target'),
                    headers=auth_json.get_xsrf_header('target'),
                    cookies=auth_json.get_cookies('target'),
                    dsm_id=[target_datastore['id'] for target_datastore in target_datastores if
                            target_datastore['code'] == source_datastore['code']][0],
                    file_path=excel_path,
                    type='add'
                )
                datastore.upload_excel(
                    base_url=auth_json.get_base_url('target'),
                    headers=auth_json.get_xsrf_header('target'),
                    cookies=auth_json.get_cookies('target'),
                    dsm_id=[target_datastore['id'] for target_datastore in target_datastores if
                            target_datastore['code'] == source_datastore['code']][0],
                    file_path=excel_path,
                    type='update'
                )
                remove(excel_path)

        return Response({
            'success': True,
            'message': 'datastore values migrated successfully',
        }, status=status.HTTP_200_OK)
