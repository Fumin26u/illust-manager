from api.model import db, UserPlatformAccount, UserPlatformAccountDlLog
from api.service.pixiv.dlImage import dlImage
from api.service.pixiv.getImage import getImage

from api.utils.getNowTime import getNowTime
from api.utils.getRootDir import getRootDir
from api.utils.makeZip import makeZip 

import os
from pixivpy3 import AppPixivAPI
from dotenv import load_dotenv

rootDir = getRootDir()
    
def getPost(user, searchQuery):
    userPlatformAccount = __getUserPlatformAccount(user['id'])
    if not userPlatformAccount:
        return False
    
    latestGetPosts = __getUserPlatformAccountDlLog(userPlatformAccount['id'])
    if not latestGetPosts:
        return False
        
    try:
        pixivpy = __connect_pixivpy_api()
        
        illust = getImage(pixivpy, searchQuery, latestGetPosts)
        return illust
    except Exception as e:
        return False
    
async def download(images):       
    nowTime = getNowTime()
    downloadPath = dict(
        image = f"{rootDir}/downloads/pixiv/images/{nowTime}",
        zip = f"{rootDir}/downloads/pixiv/zip/{nowTime}"
    )
    
    try:
        pixivpy = __connect_pixivpy_api()
        
        dlResult = await dlImage(pixivpy, f"{downloadPath['image']}", images)
        if dlResult['error']:
            return False
        
        zipFilePath = makeZip(f"{downloadPath['image']}", f"{downloadPath['zip']}")
        return zipFilePath
    except Exception as e:
        return False

def update(user_id, latestGetPosts, downloadImagesCount, platform = 'pixiv'):
    userPlatformAccount = __getUserPlatformAccount(user_id, platform)
    if not userPlatformAccount:
        return False
    
    dlCount = userPlatformAccount['dl_count'] + 1
    imagesCount = userPlatformAccount['get_images_count'] + downloadImagesCount 
    nowTime = getNowTime()
    
    (db.session
        .query(UserPlatformAccount)
        .filter_by(id = userPlatformAccount['id'])
        .update(dict(
            dl_count = dlCount,
            images_count = imagesCount
        ))
    )
    
    for post in latestGetPosts:
        db.session.add(
            UserPlatformAccountDlLog(
                user_platform_account_id = userPlatformAccount['id'],
                post_id = post['post_id'],
                downloaded_at = nowTime
            )
        )
    
    db.session.commit()
    return {'content': 'update success'}

def __connect_pixivpy_api():
    pixivpy = AppPixivAPI()
    pixivpy.auth(refresh_token = os.getenv('PIXIVPY_REFRESH_TOKEN'))
    
    return pixivpy

def __getUserPlatformAccount(user_id, platform = 'pixiv'):
    return (
        UserPlatformAccount.query
            .filter_by(
                user_id = user_id, 
                platform = platform
            )
            .first()
    )
    
def __getUserPlatformAccountDlLog(userPlatformAccountId, limit = 10):
    return (
        UserPlatformAccountDlLog.query
            .with_entities(UserPlatformAccountDlLog.post_id)
            .filter_by(user_platform_account_id = userPlatformAccountId)
            .order_by(UserPlatformAccountDlLog.downloaded_at.desc())
            .limit(limit)
            .all()
    )