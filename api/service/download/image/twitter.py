import os, random, string
import asyncio, aiohttp, aiofiles
from api.utils.string import generateRandomString

# format引数が付いている画像URLから、どの形式でフォーマットされているかを取得
def __getFormatMethod(url):
    target = 'format='
    index = url.find(target)
    if (index != -1) and index + len(target) + 3 <= len(url):
        formatMethod = url[index + len(target):index + len(target) + 3]
        if formatMethod == 'jpg':
            return 'jpg'
        elif formatMethod == 'jpe':
            return 'jpeg'
        elif formatMethod == 'jfi':
            return 'jfif'
        elif formatMethod == 'web':
            return 'webp'
        elif formatMethod == 'png':
            return 'png'
        else:
            return 'jpg'
    else:
        return 'jpg'

async def download(session, illust, savePath):
    try:
        await asyncio.sleep(1)
        async with session.get(illust, timeout=30, ssl=False) as response:
            if response.status == 200:
                fileName = f"{generateRandomString(12)}.{__getFormatMethod(illust)}"
                filePath = f"{savePath}/{fileName}"
                async with aiofiles.open(filePath, 'wb') as file:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        await file.write(chunk)
                return {'error': False}
            else:
                print('画像の保存に失敗しました。')
                return {'error': True}
    except Exception as e:
        print(f'画像の保存中にエラーが発生しました: {str(e)}')
        return {'error': True}

async def downloadImage(savePath, illusts):
    if not os.path.exists(savePath):
        os.mkdir(savePath)
    async with aiohttp.ClientSession() as session:
        for illust in illusts[::-1]:
            response = await download(session, illust, savePath)
            if response['error']:
                return {'error': True, 'content': 'download failed'}
    return {'error': False, 'content': 'download success'}