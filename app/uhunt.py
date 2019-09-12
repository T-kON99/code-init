import sys
import mechanize
import urllib
from urllib.request import urlretrieve
import app.read as read
import config.config as config
import app.utils as utils
import requests
import os

UHUNT_ROOT = 'https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem='
FILE_SAVE_PATH = f'{config.ROOT}/problems'

def displayHelp():
    pass

def getPdf(problem_no: int):
    pass

def uhunt(problem_no: int, fileType: str, overwrite: bool = False):
    try:
        os.makedirs(FILE_SAVE_PATH, exist_ok=True)
    except FileExistsError:
        pass
    #   Constants
    SRC_LANG = config.lang.get(fileType)
    assert SRC_LANG != None, 'Unsupported language'
    SRC_FILE_PATH = f'{config.ROOT}/{problem_no}.{SRC_LANG}'
    UHUNT_PDF_URL = f'https://uva.onlinejudge.org/external/{str(problem_no)[0:-2]}/p{problem_no}.pdf'
    FILE_PDF_PATH = f'{FILE_SAVE_PATH}/{problem_no}.pdf'

    if overwrite or not os.path.isfile(SRC_FILE_PATH):
        #   Download pdf.
        if overwrite or not os.path.isfile(FILE_PDF_PATH):
            r = requests.get(UHUNT_PDF_URL, stream = True)
            assert r.status_code == 200, 'Bad problem number'
            with open(FILE_PDF_PATH,"wb") as pdf: 
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk: 
                        pdf.write(chunk)
        else:
            print(f'{problem_no}.pdf exist')
        #   Convert to txt to extract problem details. Will be written as comment in the following source code file.
        FILE_CONVERT_TEXT_PATH = f'{FILE_SAVE_PATH}/{problem_no}.txt'
        if  overwrite or not os.path.isfile(FILE_CONVERT_TEXT_PATH):
            read.pdfToText(FILE_PDF_PATH, FILE_CONVERT_TEXT_PATH)
        with open(FILE_CONVERT_TEXT_PATH, mode='r', encoding='utf8') as text_file:
            problem_details = '\n'.join([_.strip().split('\n')[0] if _.strip().split('\n')[0] not in ['Sample Input', 'Input', 'Sample Output', 'Output'] else '\n' + _.strip().split('\n')[0] for _ in text_file.readlines()])
        os.remove(FILE_CONVERT_TEXT_PATH)

        # Write code depending on the lang given.
        with open(SRC_FILE_PATH, mode='w', encoding='utf8') as src_file:
            src_file.write(utils.insert_src(SRC_LANG, problem_details))
    else:
        print(f'{problem_no}.{SRC_LANG} exist')

if __name__ == "__main__":
    displayHelp()