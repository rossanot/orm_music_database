import os
from typing import Dict
import yaml
import zipfile


def load_yaml(FILE_PATH: str) -> Dict:
    """Load all contents of yaml file

    :param FILE_PATH: yaml file PATH
    :return: yaml file contents
    """
    with open(FILE_PATH) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def request_kaggle_dataset(
        credentials: Dict,
        params: Dict
        ) -> None:
    """Get dataset from Kaggle API

    :param params: Kaggle API params
    :type params: Dict
    """
    os.environ['KAGGLE_USERNAME'] = credentials['kaggle']['KAGGLE_USERNAME']
    os.environ['KAGGLE_KEY'] = credentials['kaggle']['KAGGLE_KEY']

    import kaggle

    kaggle.api.dataset_download_file('/'.join([params['user'], params['dataset_name']]),
                                     file_name=params['file_name'],
                                     path=params['path'])


def unzip_file(
          file_path: str,
          destination_path: str
          ) -> None:
    """Unzip file

    :param file_path: file to unzip
    :type file_path: str
    :param destination_path: path to store unzipped file:
    :type destination_path: str
    """
    with zipfile.ZipFile(file_path, 'r') as file:
        file.extractall(destination_path)

    os.remove(file_path)
