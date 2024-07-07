from api.model import db, UserPlatformAccount, UserPlatformAccountDlLog
import api.service.twitter.selenium.getTweet
import api.service.twitter.selenium.login
from api.service.twitter.dlImage import dlImages

from api.utils.driver import setDriver
from api.utils.getNowTime import getNowTime
from api.utils.getRootDir import getRootDir
from api.utils.makeZip import makeZip 

import os
from dotenv import load_dotenv

rootDir = getRootDir()
load_dotenv()
    
def getTweet(user_id, searchQuery):
    userPlatformAccount = getUserPlatformAccount(user_id)
    if not userPlatformAccount:
        return False
    
    latestGetTweets = __getUserPlatformAccountDlLog(userPlatformAccount['id'])
    if not latestGetTweets:
        return False
    latestGetTweets = [item for latestGetTweet in latestGetTweets for item in latestGetTweet]
    
    DRIVER = setDriver()
    # Twitterのリンク
    TWITTER_PATH = 'https://x.com'
    
    try:
        api.service.twitter.selenium.login.login(
            DRIVER, 
            userPlatformAccount['platform_id'],
            userPlatformAccount['platform_password'], 
            f"{TWITTER_PATH}/i/flow/login",
            os.getenv('TEL')
        )   
        
        tweets = api.service.twitter.selenium.getTweet.getTweet(
            DRIVER,
            searchQuery,
            latestGetTweets,
            f"{TWITTER_PATH}/{searchQuery['twitterID']}/likes"
        )
        
        return tweets
        
    except Exception as e:
        return False
    
async def download(images):       
    nowTime = getNowTime()
    downloadPath = dict(
        image = f"{rootDir}/downloads/twitter/images/{nowTime}",
        zip = f"{rootDir}/downloads/twitter/zip/{nowTime}"
    )
    
    dlResult = await dlImages(f"{downloadPath['image']}", images)
    if dlResult['error']:
        return False
    
    makeZip(f"{downloadPath['image']}", f"{downloadPath['zip']}.zip")
    return nowTime

def update(user_id, latestGetTweets, downloadImagesCount, platform = 'twitter'):
    userPlatformAccount = getUserPlatformAccount(user_id, platform)
    if not userPlatformAccount:
        return False
    
    dlCount = userPlatformAccount['dl_count'] + 1
    imagesCount = userPlatformAccount['get_images_count'] + downloadImagesCount 
    nowTime = getNowTime()
    
    (db.session
        .query(UserPlatformAccount)
        .filter_by(id = userPlatformAccount['id'])
        .update(dict(
            dl_count = str(dlCount),
            get_images_count = str(imagesCount)
        ))
    )
    
    for tweet in latestGetTweets:
        db.session.add(
            UserPlatformAccountDlLog(
                user_platform_account_id = userPlatformAccount['id'],
                post_id = tweet,
                downloaded_at = nowTime
            )
        )
    
    db.session.commit()
    return {'content': 'update success'}

def downloadZip(response, timestamp):
    zipPath = f"{rootDir}/downloads/twitter/zip/{timestamp}.zip"
    
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(zipPath)}'
    response.data = open(zipPath, 'rb').read()
    
    return response

def getUserPlatformAccount(user_id, platform = 'twitter'):
    return (
        UserPlatformAccount.query
            .filter_by(
                user_id = user_id, 
                platform = platform
            )
            .first()
            .to_dict()
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