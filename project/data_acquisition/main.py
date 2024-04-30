from importlib import resources
from pathlib import Path
from project.data_acquisition.utils import (load_yaml,
                                            request_kaggle_dataset,
                                            unzip_file)


CRED_PATH = 'project/data_acquisition/credentials.yml'
PARAMS_PATH = 'project/data_acquisition/parameters.yml'


def main():
    credentials = load_yaml(CRED_PATH)
    params = load_yaml(PARAMS_PATH)['kaggle_parms']

    FILE_PATH = resources.path('project.data', params['file_name'] + '.zip')
    request_kaggle_dataset(credentials, params)
    
    unzip_file(FILE_PATH, params['path'])


if __name__ == '__main__':
    main()

