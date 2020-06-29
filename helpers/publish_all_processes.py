import json

import requests

from helpers.authenticate import re_auth
from helpers.modify_auth_json import ModifyAuthJson


class UpdateProcessMaster():
    def __init__(self):
        re_auth('target')
        self.auth_json = ModifyAuthJson()
        self.process_master_ids = []
        self.process_versions = []

    def get_process_config(self):
        response = requests.get(
            self.auth_json.get_base_url('target') + 'v1/app/rest/process_master_config',
            cookies=self.auth_json.get_cookies('target')
        )
        if response.status_code != 200:
            Exception('Cannot get list of process masters')
        response_body = json.loads(response.content)
        if 'message' not in json.loads(response.content):
            self.process_master_ids = [process_master['id'] for process_master in json.loads(response.content)]

    def get_process_versions(self):
        for process_master_id in self.process_master_ids:
            re_auth('target')
            params = {'calledFrom': 'master',
                      'pageNo': 0,
                      'processMasterId': process_master_id,
                      'recordsPerPage': 10,
                      'sortType': 'DESC'}
            response = requests.get(self.auth_json.get_base_url('target') + 'v1/app/rest/process/versionPage',
                                    params=params,
                                    cookies=self.auth_json.get_cookies('target')
                                    )
            if response.status_code != 200 and response.status_code != 404:
                raise Exception('Cannot get list of process masters')
            if response.status_code == 200:
                self.process_versions += json.loads(response.content)['content']

    def publish_processes(self):
        for process_version in self.process_versions:
            if process_version['type'] == 'Draft':
                re_auth('target')
                headers = self.auth_json.get_xsrf_header('target')
                headers['Content-Type'] = "application/json"
                process_version['addPreviousVersion'] = False
                process_version['type'] = 'Deployed'
                process_version['updateType'] = 'normalUpdate'
                response = requests.post(self.auth_json.get_base_url('target') + 'v1/app/rest/process/version',
                                         data=json.dumps(process_version),
                                         headers=headers,
                                         cookies=self.auth_json.get_cookies('target')
                                         )
                if response.status_code != 200:
                    raise Exception('Error in publishing process master version')
