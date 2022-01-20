import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv

class GoogleSheet:


        def __init__(self, account_file: str, id: str, scopes=None):
                self._scopes = [*scopes] if scopes else None
                self._account_file = account_file
                self.id = id
                self._credentials = (service_account.Credentials
                                    .from_service_account_file(account_file, 
                                                               scopes=scopes))
                self.sheet = (build('sheets', 'v4', credentials=self.credentials)
                              .spreadsheets())

        def getValues(self, range:str) -> dict:
            return (self.sheet
                        .values()
                        .get(spreadsheetId=self.id,range=range)
                        .execute())    

        def putValues(self, range:str, input_option:str, body_values:dict) -> None:
                (planilha.sheet
                         .values()
                         .update(spreadsheetId=planilha.id, 
                                 range=range, 
                                 valueInputOption=input_option, 
                                 body=body_values)
                         .execute())
                return None

load_dotenv()
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                                    'keys.json')
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
planilha = GoogleSheet(SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, SCOPES)

result = planilha.getValues("Livros!A:A")
#caso de erro
values = result.get('values', [])
headers, books = (result['values'][0],
                  [i[0] for i in result['values'][1:]])

body_values = {"values":[[*headers,'Pontuação']]+[[book,'0'] for book in books]}
response = (planilha.putValues(range="Classificação!A1", 
                               valueInputOption="USER_ENTERED", 
                               body=body_values)
)
