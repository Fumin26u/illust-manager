import api.service.download.image.twitter
import api.service.download.image.pixiv
import api.service.download.image.local
from api.service.download.zip.createZip import createZip
from api.utils.string import getNowTime, getRootDir

async def download(images, platform):
    nowTime = getNowTime()
    rootDir = getRootDir()
    downloadPath = dict(
        image = f"{rootDir}/downloads/{platform}/images/{nowTime}",
        zip = f"{rootDir}/downloads/{platform}/zip/{nowTime}"
    )
    
    if platform == 'twitter':
        response = await api.service.download.image.twitter.downloadImage(downloadPath['image'], images)
    elif platform == 'pixiv':
        response = await api.service.download.image.pixiv.downloadImage(downloadPath['image'], images)
    elif platform == 'local':
        response = await api.service.download.image.local.importImage(downloadPath['image'], images)
    else:
        return {'error': True, 'content': 'invalid platform'}
    
    if platform == 'local':
        return response
    if response['error']:
        return response
    
    return {'error': False, 'now_time': nowTime}