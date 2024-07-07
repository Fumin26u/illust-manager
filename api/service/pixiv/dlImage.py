import os, random, string, asyncio
# pixivpy: pixivからデータを抽出するAPI
from pixivpy3 import *
# import APIkey
from dotenv import load_dotenv

# Auth接続
aapi = AppPixivAPI()
aapi.auth(refresh_token = os.getenv('PIXIVPY_REFRESH_TOKEN'))

# ランダム文字列の生成
def generateRandomString(strLength: int) -> str:
    strArray = [random.choice(string.ascii_letters + string.digits) for i in range(strLength)]
    return ''.join(strArray)

async def dlImage(savePath, illusts):
    try:
        # 指定されたフォルダが存在しない場合新規作成
        if not os.path.exists(savePath):
            os.mkdir(savePath)
        await asyncio.sleep(1)
        
        # ダウンロード処理
        for illust in illusts:
            # ファイル名の設定
            file_name = generateRandomString(12) + '.jpg'
            # ダウンロード処理
            aapi.download(illust, path = savePath, name = file_name)
            await asyncio.sleep(1)

        return {'content': 'download success'}
    except Exception as e:
        return {'error': True, 'content': e}
