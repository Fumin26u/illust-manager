from api.model import db
import api.service.twitter.selenium.getTweet
import api.service.twitter.selenium.login
from api.service.twitter.dlImage import dlImages

import api.service.userPlatformAccount
import api.service.userPlatformAccountDlLog

from api.utils.driver import setDriver
from api.utils.getNowTime import getNowTime
from api.utils.getRootDir import getRootDir
from api.utils.makeZip import makeZip 

import os
from dotenv import load_dotenv

rootDir = getRootDir()
load_dotenv()
    
def getTweet(user_id, searchQuery):
    userPlatformAccount = api.service.userPlatformAccount.select(user_id, 'twitter')
    if not userPlatformAccount:
        return False
    
    latestGetTweets = api.service.userPlatformAccountDlLog.select(userPlatformAccount['id'])
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
    
    for tweet in latestGetTweets:
        api.service.userPlatformAccountDlLog.create(
            userPlatformAccount['id'],
            tweet,
            nowTime
        )
    
    db.session.commit()
    return {'content': 'update success'}

def downloadZip(response, timestamp):
    zipPath = f"{rootDir}/downloads/twitter/zip/{timestamp}.zip"
    
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(zipPath)}'
    response.data = open(zipPath, 'rb').read()
    
    return response