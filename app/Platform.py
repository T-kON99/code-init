from abc import ABC, abstractmethod
import config.config as config
import os
import requests
import time
import app.read as read
from bs4 import BeautifulSoup

class Platform(ABC):
    def __init__(self, name: str = None, url: str = None):
        assert isinstance(name, str) and isinstance(url, str), f'[ERROR]: Invalid type, expected str but got {name}: {type(name)}, {url}: {type(url)} instead'
        self.PLATFORM_NAME = name
        self.URL = url
        self.__ASSET_PATH = f'{config.ROOT}/{config.RESOURCES_DIR_NAME}/{self.PLATFORM_NAME}/'
    
    def get_problem_no(self, problem_no: int, timeout_attempt: int = 5, overwrite: bool = False):
        while timeout_attempt > 0:
            try:
                res = self.handler(problem_no, overwrite=overwrite)
                return res
            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)
            except requests.exceptions.Timeout:
                timeout_attempt -= 1
                time.sleep(1)
            except requests.exceptions.TooManyRedirects:
                raise SystemExit('ERROR: Bad problem number redirecting to too many places')
            except requests.exceptions.RequestException as e:
                # catastrophic error. bail.
                raise SystemExit(e)

    @abstractmethod
    def handler(self, problem_no: int, overwrite: bool = False):
        pass

    def prepare_asset(self, file_name: str):
        assert isinstance(file_name, str), f'Invalid type. Filename {file_name} is not of type string.'
        os.makedirs(self.__ASSET_PATH, exist_ok=True)
        return self.__ASSET_PATH + file_name

    def _download_file(self, url: str, path_to_write: str, overwrite: bool):
        if overwrite or not os.path.isfile(path_to_write):
            r = requests.get(url, stream=True)
            r.raise_for_status()
            assert r.status_code == 200, f'[ERROR]: Bad URL {url}'
            os.makedirs(os.path.dirname(path_to_write), exist_ok=True)
            with open(path_to_write,"wb") as file: 
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: 
                        file.write(chunk)
            print(f'[INFO]: Downloaded asset file {os.path.abspath(path_to_write)}')
            return path_to_write
        else:
            print(f'[INFO]: {os.path.abspath(path_to_write)} already exists, skipping download')
            return None

class Uhunt(Platform):
    def __init__(self):
        NAME = 'uhunt'
        super().__init__(NAME, config.PLATFORM_URLS[NAME])

    def handler(self, problem_no: int, overwrite: bool = False):
        #   uva uhunt files comes in pdf format, hence needs to be downloaded first
        UHUNT_PDF_URL = self.URL + f'{str(problem_no)[0:-2]}/p{problem_no}.pdf'
        FILE_PDF_PATH = self.prepare_asset(f'{problem_no}.pdf')
        self._download_file(
            UHUNT_PDF_URL,
            FILE_PDF_PATH,
            overwrite
        )
        #   Convert to txt to extract problem details. Will be written as comment in the following source code file.
        print(f'[INFO]: Converting PDF to TXT file to extract the text information')
        TEMP_FILE_CONVERT_TEXT_PATH = f'{config.ROOT}/assets/{self.PLATFORM_NAME}/p{problem_no}.txt'
        print(f'[INFO]: Creating temporary TXT file {TEMP_FILE_CONVERT_TEXT_PATH}')
        if  overwrite or not os.path.isfile(TEMP_FILE_CONVERT_TEXT_PATH):
            read.pdfToText(FILE_PDF_PATH, TEMP_FILE_CONVERT_TEXT_PATH)
        with open(TEMP_FILE_CONVERT_TEXT_PATH, mode='r', encoding='utf8') as text_file:
            problem_details = '\n'.join([' '.join(_.split()) for _ in text_file.readlines()])
            # problem_details = '\n'.join([_.strip().split('\n')[0] if _.strip().split('\n')[0] not in ['Sample Input', 'Input', 'Sample Output', 'Output'] else '\n' + _.strip().split('\n')[0] for _ in text_file.readlines()])
        os.remove(TEMP_FILE_CONVERT_TEXT_PATH)
        print(f'[INFO]: Deleted temporary TXT file {TEMP_FILE_CONVERT_TEXT_PATH}')
        return {
            'title': str(problem_no),
            'content': problem_details
        }

class ProjectEuler(Platform):
    def __init__(self):
        NAME = 'projecteuler'
        super().__init__(NAME, config.PLATFORM_URLS[NAME])
        
    def handler(self, problem_no: int, overwrite: bool = False):
        res = requests.get(self.URL + f'problem={problem_no}')
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        problem = soup.body.find(id='container').find(id='content')
        problem_info = problem.find(id='problem_info')
        if problem_info is not None:
            problem_title, problem_content = problem.find('h2'), problem.find(class_='problem_content')
            problem_asset = problem_content.find('a')
            if problem_asset is not None:
                #   Download asset if exists to respective problems file according to problem number.
                asset_url = problem_asset.get('href')
                asset_filename = self.prepare_asset(os.path.basename(asset_url))
                self._download_file(
                    self.URL + asset_url, 
                    asset_filename, 
                    overwrite
                )
            return {
                'title': problem_title.text.strip('\n'),
                'content': problem_content.text.strip('\n')
            }
        else:
            raise requests.exceptions.HTTPError('ERROR: Invalid problem number given')

if __name__ == "__main__":
    a = Uhunt()
    print(a.get_problem_no(10712))
    b = ProjectEuler()
    print(b.get_problem_no(1))