import os
import json

ROOT = os.getcwd()
RESOURCES_DIR_NAME = 'assets'
PLATFORM_URLS = {
    'projecteuler': 'https://projecteuler.net/',
    'uhunt': 'https://onlinejudge.org/external/'
}

with open(f'{ROOT}/config/config.json') as file:
    setup: dict = json.load(file)
    
comments = setup.get('comment')
init_code = setup.get('code')
lang = setup.get('lang')