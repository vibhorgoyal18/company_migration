from _datetime import datetime

import pandas as pd
import requests

from company_migration.settings import BASE_DIR

temp_files_path = BASE_DIR + '/temp_files/'
def env_variables_to_dataframe(variables):
    variables_df = pd.DataFrame(variables)
    variables_df.drop(['id', 'companyId'], inplace=True, axis=1)
    variables_df.rename(columns={'type': 'Type'}, inplace=True)
    return variables_df


def download_file(url):
    response = requests.get(url)
    assert response.status_code == 200, 'Cannot download file: ' + url
    file_name = temp_files_path + 'datastore_' + datetime.now().strftime("%d%m%Y_%H%M%S") + '.csv'

    with open(file_name, "wb") as outfile:
        outfile.write(response.content)
        outfile.close()

    return file_name
