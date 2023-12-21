import json
from datetime import datetime
from api.account.accountInfo import AccountInfo

class AccountManager:
    def __init__(self, jsonPath = 'api/account/userdata.json'):
        self.jsonPath = jsonPath
        self.account = self.loadAccount(jsonPath)
        
    def loadAccount(self, jsonPath):
        try:
            with open(jsonPath, 'r') as file:
                accountData = json.load(file)
                return AccountInfo(
                        accountData['user_name'],
                        datetime.strptime(accountData['created_at'], '%Y-%m-%d %H:%M:%S'),
                        accountData['dl_count'],
                        accountData['images_count'],
                        accountData['twitter'],
                        accountData['pixiv']
                    )
        except FileNotFoundError:
            return AccountInfo(None, None, None, None, None, None)
        except json.decoder.JSONDecodeError:
            return AccountInfo(None, None, None, None, None, None)
        
    def saveAccount(self):
        with open(self.jsonPath, 'w') as file:
            json.dump(self.account.toDict(), file, indent=4, ensure_ascii=False)
        
    def getSingleData(self, key):
        return self.account.toDict().get(key) if hasattr(self.account, 'toDict') else None
    
    def getPixivInfo(self):
        return self.account.pixiv if hasattr(self.account, 'pixiv') else None
    
    def update(self, key, value):
        if hasattr(self.account, key):
            setattr(self.account, key, value)
            self.saveAccount()
            return True
    
    # def create(self, id, password):
    #     return self.account.create(id, password)
    
    # def delete(self, id):
    #     return self.account.delete(id)
    
    # def update(self, id, password):
    #     return self.account.update(id, password)