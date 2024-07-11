import api.service.download.image.twitter
import api.service.download.image.pixiv
from api.service.download.zip.createZip import createZip
from api.utils.string import getNowTime, getRootDir

async def download(images, platform):
    nowTime = getNowTime()
    rootDir = getRootDir()
    downloadPath = dict(
        image = f"{rootDir}/downloads/pixiv/images/{nowTime}",
        zip = f"{rootDir}/downloads/pixiv/zip/{nowTime}"
    )
    
    if platform is 'twitter':
        nowTime = await api.service.download.image.twitter.downloadImage(images, downloadPath['image'])
    elif platform is 'pixiv':
        nowTime = await api.service.download.image.pixiv.downloadImage(images, downloadPath['image'])
    else:
        return {'error': True, 'content': 'invalid platform'}
    
    response = createZip(downloadPath['image'], downloadPath['zip'])
    if response['error']:
        return response
    
    return {'error': False, 'now_time': nowTime}