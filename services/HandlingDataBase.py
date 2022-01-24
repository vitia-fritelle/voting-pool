import __init__
import os
import json
from entities.VoteCard import VoteCard
from entities.GoogleSheets import GoogleSheet
from dotenv import load_dotenv
from functools import partial
from typing import List
from utils.keystoenv import str_to_dict

load_dotenv('..\\.env')
scopes = ['https://www.googleapis.com/auth/spreadsheets']
account_info = str_to_dict(os.environ.get('GOOGLE_ACCOUNT'))
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')

def get_headers_complete(account_info, SPREADSHEET_ID, 
                         scopes, expression: str) -> List[str]:

    sheet = GoogleSheet(account_info, SPREADSHEET_ID, scopes)
    result = sheet.getValues(expression)
    headers = result['values'][0]
    return headers

def get_vote_cards_complete(account_info, SPREADSHEET_ID, 
                            scopes, expression: str) -> List[VoteCard]:
        
    sheet = GoogleSheet(account_info, SPREADSHEET_ID, scopes)
    result = sheet.getValues(expression)
    headers, rows = (result['values'][0],
                     [i for i in result['values'][1:]])
    votecards = [VoteCard(int(row[headers.index('Pontuação')]),
                          row[headers.index('Livros')],
                          row[headers.index('Imagens')],
                          int(row[headers.index('Índices')])) 
                 for row in rows]
    return votecards

def update_google_sheet_complete(headers: list, table: list[list], 
    account_info, SPREADSHEET_ID, scopes) -> None:
    sheet = GoogleSheet(account_info, SPREADSHEET_ID, scopes)
    body_values = {"values":[headers]+table}
    sheet.putValues(range="Classificação!A1", 
                    input_option="USER_ENTERED", 
                    body_values=body_values)
    return None

get_headers = partial(get_headers_complete,account_info = account_info,
                      SPREADSHEET_ID=SPREADSHEET_ID, scopes=scopes, 
                      expression="Classificação!A:D")
get_vote_cards = partial(get_vote_cards_complete,account_info = account_info,
                         SPREADSHEET_ID=SPREADSHEET_ID, scopes=scopes, 
                         expression="Classificação!A:D")
update_google_sheet = partial(update_google_sheet_complete,account_info = account_info,
                              SPREADSHEET_ID=SPREADSHEET_ID, scopes=scopes)
