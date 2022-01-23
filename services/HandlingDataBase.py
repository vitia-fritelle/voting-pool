
import os
import os.path as path
from entities.VoteCard import VoteCard
from entities.GoogleSheets import GoogleSheet
from dotenv import load_dotenv
from functools import partial
from typing import List

load_dotenv()
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = (
        path.join(
                path.abspath(
                        path.dirname(__file__)),'keys.json'
                )
        )
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')

def get_headers_complete(SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, 
                         SCOPES, expression: str) -> List[str]:

    sheet = GoogleSheet(SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, SCOPES)
    result = sheet.getValues(expression)
    headers = result['values'][0]
    return headers

def get_vote_cards_complete(SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, 
                            SCOPES, expression: str) -> List[VoteCard]:
        
    sheet = GoogleSheet(SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, SCOPES)
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
    SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, SCOPES) -> None:
    sheet = GoogleSheet(SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, SCOPES)
    body_values = {"values":[headers]+table}
    sheet.putValues(range="Classificação!A1", 
                    input_option="USER_ENTERED", 
                    body_values=body_values)
    return None

get_headers = partial(get_headers_complete,SERVICE_ACCOUNT_FILE = SERVICE_ACCOUNT_FILE,
                      SPREADSHEET_ID=SPREADSHEET_ID, SCOPES=SCOPES, 
                      expression="Classificação!A:D")
get_vote_cards = partial(get_vote_cards_complete,SERVICE_ACCOUNT_FILE = SERVICE_ACCOUNT_FILE,
                         SPREADSHEET_ID=SPREADSHEET_ID, SCOPES=SCOPES, 
                         expression="Classificação!A:D")
update_google_sheet = partial(update_google_sheet_complete,SERVICE_ACCOUNT_FILE = SERVICE_ACCOUNT_FILE,
                              SPREADSHEET_ID=SPREADSHEET_ID, SCOPES=SCOPES)
