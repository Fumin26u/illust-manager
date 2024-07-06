from api.model import db, UserPlatformAccount, UserPlatformAccountDlLog
import api.service.twitter.selenium.getTweet
import api.service.twitter.selenium.login
from api.service.twitter.dlImage import dlImages

from api.utils.driver import setDriver
from api.utils.getNowTime import getNowTime
from api.utils.getRootDir import getRootDir
from api.utils.makeZip import makeZip 

rootDir = getRootDir()
    
def getTweet(user, searchQuery):
    userPlatformAccount = __getUserPlatformAccount(user['id'])
    if not userPlatformAccount:
        return False
    
    latestGetTweets = __getUserPlatformAccountDlLog(userPlatformAccount['id'])
    if not latestGetTweets:
        return False
    
    DRIVER = setDriver()
    # Twitterのリンク
    TWITTER_PATH = 'https://x.com/'
    
    try:
        api.service.twitter.selenium.login.login(
            DRIVER, 
            userPlatformAccount['platform_id'],
            userPlatformAccount['platform_password'], 
            f"{TWITTER_PATH}i/flow/login"
        )   
        
        tweets = api.service.twitter.selenium.getTweet.getTweet(
            DRIVER,
            searchQuery,
            latestGetTweets,
            f"{TWITTER_PATH}/likes"
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
    
    zipFilePath = makeZip(f"{downloadPath['image']}", f"{downloadPath['zip']}")
    return zipFilePath

def __getUserPlatformAccount(user_id, platform = 'twitter'):
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