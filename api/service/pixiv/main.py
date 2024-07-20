from api.service.pixiv.getImage import getImage

import api.service.userPlatformAccount
import api.service.userPlatformAccountDlLog

from api.utils.string import getNowTime, getRootDir

rootDir = getRootDir()
    
async def getPost(user_id, searchQuery):
    userPlatformAccount = api.service.userPlatformAccount.select(user_id, 'pixiv')
    if not userPlatformAccount:
        return False
    
    latestGetPosts = api.service.userPlatformAccountDlLog.select(userPlatformAccount['id'])
    if not latestGetPosts:
        return False
    latestGetPosts = [latestGetPost['post_id'] for latestGetPost in latestGetPosts]
    print(latestGetPosts)
            
    try:        
        illust = await getImage(searchQuery, latestGetPosts)
        print(illust)
        return illust
    except Exception as e:
        return e
    
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
    
    return {'content': 'update success'}