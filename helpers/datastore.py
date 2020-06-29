import json
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests


class DatastoreMigration:

    def get_existing_datastores(self, base_url, cookies, headers):
        response = requests.get(
            base_url + 'v1/app/rest/data_store_master_enabled_list',
            cookies=cookies,
            headers=headers,
        )

        if response.status_code != 200:
            raise Exception('Error getting existing datastores from source account')

        return json.loads(response.content)

    def get_datastore_attributes(self, base_url, cookies, headers, dsm_id):
        response = requests.get(
            base_url + 'v1/app/rest/data_store_attribute_master/' + str(dsm_id),
            cookies=cookies,
            headers=headers,
        )

        if response.status_code != 200:
            raise Exception('Error getting datastore details of source for datastore: ' + str(dsm_id))

        return json.loads(response.content)

    def generate_datastore_dump_report(self, base_url, cookies, headers, dsm_id, ds_attributes):

        payload = {
            "dataStoreMasterId": dsm_id,
            "reportType": "DataStoreDump",
            "dumpRequiredColumnsDTO": {
                "dsAttributes": ds_attributes,
                "basicAttributes": [],
                "maintainAttributeSequence": True
            }
        }

        headers['Content-Type'] = "application/json"

        response = requests.post(
            base_url + 'v1/app/rest/report/datastore_dump_report',
            data=json.dumps(payload),
            cookies=cookies,
            headers=headers,
        )

        if response.status_code != 200:
            raise Exception('Error generating datastore dump report for datastore: ' + str(dsm_id))

        return json.loads(response.content)

    def get_datastore_dump_download_url(self, base_url, cookies, headers, dsm_id):
        params = {
            'pageNo': 0,
            'recordsPerPage': 1,
            'sortOn': 'id',
            'sortType': 'DESC',
            'type': 'DataStoreDump'
        }
        response = requests.get(
            base_url + 'v1/app/rest/report/report_list',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception('Not able to fetch datastore dump url for datastore: ' + str(dsm_id))

        report_obj = (json.loads(response.content))['content'][0]

        assert report_obj[
                   'dsMasterId'] == dsm_id, \
            'Was successfully able to fetch datastore but the datastore id is not as expected ' + str(dsm_id)

        # request_time = datetime.strptime(report_obj['requestTime'], '%Y-%m-%d %H:%M:%S')
        # current_time = datetime.now()
        # current_time += timedelta(hours=5, minutes=30)
        # difference = (current_time - request_time).total_seconds()

        # assert difference < 120, 'Not able to fetch datastore dump url for datastore: ' + str(dsm_id)
        return report_obj['downloadLink']

    def convert_dump_to_excel(self, file_path: str, dsm_attributes):
        columns = []
        datastore_df = pd.read_csv(file_path)

        for column in datastore_df.columns:
            dsm_attribute_key = [col['key'] for col in dsm_attributes if col['label'] == column]
            if len(dsm_attribute_key) == 1:
                columns.append(dsm_attribute_key[0])
            else:
                columns.append(column)
        datastore_df.columns = columns
        datastore_df['hubs'] = np.nan
        datastore_df['Field Executive'] = np.nan
        file_path = (file_path.replace('csv', 'xls'))
        del datastore_df[' ']
        datastore_df.to_excel(file_path, index=False)

        return file_path

    def upload_excel(self, base_url, cookies, headers, file_path, dsm_id, type):
        file = {'file': ('env_variables.xls', open(file_path, 'rb'), 'application/vnd.ms-excel')}
        params = {
            'dataStoreMasterId': dsm_id,
            'type': type
        }
        response = requests.post(
            base_url + 'v1/app/rest/data_store/upload_excel',
            params=params,
            cookies=cookies,
            headers=headers,
            files=file
        )

        assert response.status_code == 200, 'Cannot upload excel for datastore with id: ' + dsm_id
