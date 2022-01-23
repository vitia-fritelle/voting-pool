from googleapiclient.discovery import build
from google.oauth2 import service_account

#Falta fazer o typing direito aqui
class GoogleSheet:


        def __init__(self, account_file:str, id:str, scopes=None):
                self._scopes = [*scopes] if scopes else None
                self._account_file = account_file
                self.id = id
                self._credentials = (service_account.Credentials
                                     .from_service_account_file(account_file, 
                                                                scopes=scopes))
                self.sheet = (
                        build('sheets', 'v4', credentials=self._credentials)
                        .spreadsheets()
                        )

        def getValues(self, range:str) -> dict:
            return (self.sheet
                        .values()
                        .get(spreadsheetId=self.id,range=range)
                        .execute())    

        def putValues(self, range:str, 
                      input_option:str, body_values:dict) -> None:
                (self.sheet
                     .values()
                     .update(spreadsheetId=self.id, 
                             range=range, 
                             valueInputOption=input_option, 
                             body=body_values)
                     .execute())
                return None

