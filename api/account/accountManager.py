import json
from datetime import datetime
from api.account.accountInfo import AccountInfo

class AccountManager:
    def __init__(self, jsonPath = 'api/account/userdata.json'):
        self.jsonPath = jsonPath
        self.account = self.loadAccount(jsonPath)
        
    def loadAccount(self, jsonPath):
        try:
            with open(jsonPath, 'r', encoding='utf-8') as file:
                accountData = json.load(file)
                
                created_at = datetime.strptime(accountData['created_at'], '%Y-%m-%d %H:%M:%S') if accountData['created_at'] != '' else ''
                updated_at = datetime.strptime(accountData['updated_at'], '%Y-%m-%d %H:%M:%S') if accountData['updated_at'] != '' else ''
                
                return AccountInfo(
                        accountData['user_name'],
                        created_at,
                        updated_at,
                        accountData['twitter_password'],
                        accountData['pixiv_password'],
                        accountData['dl_count'],
                        accountData['images_count'],
                        accountData['twitter'],
                        accountData['pixiv']
                    )
        except FileNotFoundError:
            return AccountInfo(None, None, None, None, None, None, None, None)
        except json.decoder.JSONDecodeError:
            return AccountInfo(None, None, None, None, None, None, None, None)
        
    def saveAccount(self):
        with open(self.jsonPath, 'w', encoding='utf-8') as file:
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
        
    def delete(self):
        # ファイルを読み込む
        try:
            with open(self.jsonPath, 'r+', encoding='utf-8') as file:
                data = json.load(file)

                # 各キーの値をチェックして適切な型で初期化する
                for key, value in data.items():
                    if isinstance(value, str):
                        data[key] = ''
                    elif isinstance(value, int):
                        data[key] = 0
                    elif isinstance(value, list):
                        data[key] = []

                # ファイルポインタを先頭に戻す
                file.seek(0)

                # 変更をファイルに保存する
                json.dump(data, file, indent=4, ensure_ascii=False)
                file.truncate()

                # アカウントオブジェクトも更新する
                self.account = self.loadAccount(self.jsonPath)

        except FileNotFoundError:
            print("ファイルが見つかりませんでした。")
        except json.decoder.JSONDecodeError:
            print("JSONデコードエラーが発生しました。")