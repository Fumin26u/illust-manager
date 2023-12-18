import json
from datetime import datetime
from api.account.accountInfo import AccountInfo

class AccountManager:
    def __init__(self, jsonPath = 'api/account/userdata.json'):
        self.account = self.loadAccount(jsonPath)
        
    def loadAccount(self, jsonPath):
        try:
            with open(jsonPath, 'r') as file:
                accountData = json.load(file)
                account = AccountInfo(
                        accountData['user_name'],
                        datetime.strptime(accountData['created_at'], '%Y-%m-%d %H:%M:%S'),
                        accountData['dl_count'],
                        accountData['images_count'],
                        accountData['twitter'],
                        accountData['pixiv']
                )
                return account
        except FileNotFoundError:
            return {}
        except json.decoder.JSONDecodeError:
            return {}
        
    def getUsername(self):
        return self.account.user_name if hasattr(self.account, 'user_name') else None
    
    # def create(self, id, password):
    #     return self.account.create(id, password)
    
    # def delete(self, id):
    #     return self.account.delete(id)
    
    # def update(self, id, password):
    #     return self.account.update(id, password)