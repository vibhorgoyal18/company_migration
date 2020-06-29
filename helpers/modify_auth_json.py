import json
import os

from company_migration.settings import BASE_DIR


class ModifyAuthJson():

    def __init__(self):
        self.json_data = {}
        self.file_name = BASE_DIR + '/temp_files/auth.json'
        if not os.path.exists(BASE_DIR + '/temp_files'):
            os.mkdir(BASE_DIR + '/temp_files')

        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w') as outfile:
                json.dump({}, outfile)
                outfile.close()

        self.get_auth_data()

    def get_auth_data(self):
        with open(self.file_name) as file:
            self.json_data = json.load(file)
        return self.json_data

    def set_auth_data(self, data):
        self.json_data = data
        with open(self.file_name, 'w') as outfile:
            json.dump(self.json_data, outfile)
            outfile.close()

    def get_xsrf_header(self, server_type):
        self.get_auth_data()
        return {
            'X-XSRF-TOKEN': self.json_data[server_type]['cookies']['XSRF-TOKEN']

        }

    def get_base_url(self, server_type):
        self.get_auth_data()
        return self.json_data[server_type]['base_url']

    def get_username(self, server_type):
        self.get_auth_data()
        return self.json_data[server_type]['username']

    def get_password(self, server_type):
        self.get_auth_data()
        return self.json_data[server_type]['password']

    def get_cookies(self, server_type):
        self.get_auth_data()
        return self.json_data[server_type]['cookies']

    def get_company_id(self, server_type):
        self.get_auth_data()
        return self.json_data[server_type]['cookies']['FAREYE_CMP_ID']