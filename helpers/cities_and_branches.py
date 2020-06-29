import json

import requests


class CitiesAndBranches:

    def __init__(self, source_base_url, source_cookies, source_headers, target_base_url, target_cookies,
                 target_headers):
        self.source_base_url, self.source_cookies, self.source_headers = source_base_url, source_cookies, source_headers
        self.target_base_url, self.target_cookies, self.target_headers = target_base_url, target_cookies, target_headers
        self.source_cities = self.get_cities(source_base_url, source_cookies)
        self.target_cities = self.get_cities(target_base_url, target_cookies)
        self.post_cities()
        self.source_branches =self.get_branches('source')
        self.target_branches = self.get_branches('target')

    def get_cities(self, base_url, cookies):
        response = requests.get(
            url=base_url + "v1/app/rest/cities",
            cookies=cookies
        )
        if response.status_code != 200:
            raise Exception('error in getting cities')

        return json.loads(response.content)

    def post_cities(self):
        target_city_names = [city['name'] for city in self.target_cities]
        for source_city in self.source_cities:
            if source_city['name'] not in target_city_names:
                response = requests.post(
                    self.target_base_url + 'v1/app/rest/cities',
                    data=json.dumps({
                        'name': source_city['name'],
                        'enabled': source_city['enabled']
                    }),
                    headers=self.target_headers,
                    cookies=self.target_cookies
                )
                if response.status_code != 200:
                    raise Exception('Cannot add cities on target server')
                self.target_cities.append(json.loads(response.content))

    def get_branches(self, server_type):
        branches = []
        for city in (self.source_cities if server_type == 'source' else self.target_cities):
            params = {
                'city_id': city['id'],
                'pageNo': '0',
                'recordsPerPage': '500',
                'sortOn': 'id',
                'sortType': 'DESC'
            }
            response = requests.get(
                (
                    self.source_base_url if server_type == 'source' else self.target_base_url
                ) + 'v1/app/rest/hubs/pageable',
                params=params,
                headers=self.source_headers if server_type == 'source' else self.target_headers,
                cookies=self.source_cookies if server_type == 'source' else self.target_cookies
            )
            if response.status_code != 200 and response.status_code != 204:
                raise Exception('Error in getting branches')

            if response.status_code == 200:
                branches += json.loads(response.content)['content']

        return branches

