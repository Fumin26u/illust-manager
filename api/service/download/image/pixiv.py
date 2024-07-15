import os, asyncio
# pixivpy: pixivからデータを抽出するAPI
from pixivpy3 import *
from api.driver.connectPixivpyApi import connect_pixivpy_api
# import APIkey
from dotenv import load_dotenv
from api.utils.string import generateRandomString

async def downloadImage(savePath, illusts):
    try:
        # 指定されたフォルダが存在しない場合新規作成
        if not os.path.exists(savePath):
            os.mkdir(savePath)
        await asyncio.sleep(1)
        
        # ダウンロード処理
        pixivpy = connect_pixivpy_api()
        for illust in illusts:
            # ファイル名の設定
            file_name = generateRandomString(12) + '.jpg'
            # ダウンロード処理
            pixivpy.download(illust, path = savePath, name = file_name)
            await asyncio.sleep(1)

        return {'error': False, 'content': 'download success'}
    except Exception as e:
        return {'error': True, 'content': e}
