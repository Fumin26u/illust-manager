from api.model import db
import api.service.twitter.selenium.getTweet
import api.service.twitter.selenium.login

import api.service.userPlatformAccount
import api.service.userPlatformAccountDlLog

from api.utils.driver import setDriver
from api.utils.string import getNowTime, getRootDir

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