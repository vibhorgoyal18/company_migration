import json

import requests

from helpers.modify_auth_json import ModifyAuthJson


def authenticate_company(base_url, username, password):
    body = {
        "j_username": username,
        "j_password": password,
        "remember-me": "true"
    }
    session = requests.Session()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = session.post(
        url=base_url + 'app/authentication',
        data=body,
        headers=headers
    )

    return response.status_code, response.cookies, None if response.status_code == 200 else json.loads(response.content)


def get_account(base_url, cookies):
    response = requests.get(
        url=base_url + 'app/authentication',
        cookies=cookies
    )
    assert response.status_code != 200, 'Not able to authenticate source server'
    return response.cookies['XSRF-TOKEN']


def re_auth(server_type):
    auth_json = ModifyAuthJson()
    json_file_data = auth_json.get_auth_data()
    response_status, cookies, response_body = authenticate_company(
        base_url=auth_json.get_base_url(server_type),
        username=auth_json.get_username(server_type),
        password=auth_json.get_password(server_type),
    )
    if response_status != 200:
        raise Exception('Not able to authenticate source server')

    json_file_data[server_type]['cookies'] = cookies.get_dict()
    if server_type == 'target':
        json_file_data[server_type]['cookies']['XSRF-TOKEN'] = get_account(
            base_url=auth_json.get_base_url(server_type),
            cookies=cookies.get_dict()
        )

    auth_json.set_auth_data(json_file_data)


def get_api_key(base_url, cookies, headers):
    response = requests.get(base_url + 'v1/app/rest/user/api_key', cookies=cookies, headers=headers)
    if response.status_code != 200:
        raise Exception('Not able to get API Key')
    if len(str(response.content)) == 3:
        response = requests.post(base_url + 'v1/app/rest/user/api_key', cookies=cookies, headers=headers)
    if response.status_code != 200:
        raise Exception('Not able to get API Key')
    return json.loads(response.content)['token']
