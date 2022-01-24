import json
import re
import os
from dotenv import load_dotenv

def json_to_env(keys_path:str) -> None:
    '''This function has the only purpose of converting the json file 
    with your Google Credentials to .env
    '''
    with open(keys_path, 'r') as f:
        info = json.load(f)
    account_info = json.dumps(info)

    with open('..\.env', 'a') as f:
        f.write(f'GOOGLE_ACCOUNT={account_info}')
        
    return None

def str_to_dict(string:str) -> dict:
    
    pattern = re.compile('"([^{},"]+?)": "([^{},"]+?)"')
    return {key.replace('\\n', '\n'):value.replace('\\n', '\n') 
            for key,value in pattern.findall(string)}
