import sys, json, os, random, string, time, asyncio
# pixivpy: pixivからデータを抽出するAPI
from pixivpy3 import *
# import APIkey
import api.imagedler.pixiv.config as config

# Auth接続
aapi = AppPixivAPI()
aapi.auth(refresh_token = config.REFRESH_TOKEN)

# ランダム文字列の生成
def generateRandomString(strLength: int) -> str:
    strArray = [random.choice(string.ascii_letters + string.digits) for i in range(strLength)]
    return ''.join(strArray)

async def main(savePath, illusts):
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

    return {
        'error': False,
        'content': 'download success'
    }
