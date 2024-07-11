import api.service.download.image.twitter
import api.service.download.image.pixiv
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
    else:
        return {'error': True, 'content': 'invalid platform'}
    if response['error']:
        return response
    
    response = createZip(downloadPath['image'], downloadPath['zip'])
    if response['error']:
        return response
    
    return {'error': False, 'now_time': nowTime}