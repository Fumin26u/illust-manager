from api.model import db
from api.service.pixiv.dlImage import dlImage
from api.service.pixiv.getImage import getImage

import api.service.userPlatformAccount
import api.service.userPlatformAccountDlLog

from api.utils.getNowTime import getNowTime
from api.utils.getRootDir import getRootDir
from api.utils.makeZip import makeZip 

import os
from pixivpy3 import AppPixivAPI

rootDir = getRootDir()
    
async def getPost(user_id, searchQuery):
    userPlatformAccount = api.service.userPlatformAccount.select(user_id, 'pixiv')
    if not userPlatformAccount:
        return False
    
    latestGetPosts = api.service.userPlatformAccountDlLog.select(userPlatformAccount['id'])
    if not latestGetPosts:
        return False
    latestGetPosts = [item for latestGetPost in latestGetPosts for item in latestGetPost]
        
    try:
        pixivpy = __connect_pixivpy_api()
        
        illust = await getImage(pixivpy, searchQuery, latestGetPosts)
        return illust
    except Exception as e:
        return False
    
async def download(images):       
    nowTime = getNowTime()
    downloadPath = dict(
        image = f"{rootDir}/downloads/pixiv/images/{nowTime}",
        zip = f"{rootDir}/downloads/pixiv/zip/{nowTime}"
    )
    
    pixivpy = __connect_pixivpy_api()
    
    dlResult = await dlImage(pixivpy, f"{downloadPath['image']}", images)
    if dlResult['error']:
        return False

    print(makeZip(f"{downloadPath['image']}", f"{downloadPath['zip']}.zip"))
    return nowTime

def update(user_id, latestGetPosts, downloadImagesCount, platform = 'pixiv'):
    userPlatformAccount = api.service.userPlatformAccount.select(user_id, platform)
    if not userPlatformAccount:
        return False
    
    dlCount = userPlatformAccount['dl_count'] + 1
    imagesCount = userPlatformAccount['get_images_count'] + downloadImagesCount 
    nowTime = getNowTime()
    
    api.service.userPlatformAccount.update(userPlatformAccount['id'], dict(
        dl_count = dlCount,
        get_images_count = imagesCount,    
    ))
    
    for post in latestGetPosts:
        api.service.userPlatformAccountDlLog.create(
            userPlatformAccount['id'],
            post,
            nowTime
        )
    
    db.session.commit()
    return {'content': 'update success'}

def downloadZip(response, timestamp):
    zipPath = f"{rootDir}/downloads/pixiv/zip/{timestamp}.zip"
    
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(zipPath)}'
    response.data = open(zipPath, 'rb').read()
    
    return response

def __connect_pixivpy_api():
    pixivpy = AppPixivAPI()
    pixivpy.auth(refresh_token = os.getenv('PIXIVPY_REFRESH_TOKEN'))
    
    return pixivpy