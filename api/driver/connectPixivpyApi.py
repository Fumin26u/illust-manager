from pixivpy3 import AppPixivAPI
import os

def connect_pixivpy_api():
    pixivpy = AppPixivAPI()
    pixivpy.auth(refresh_token = os.getenv('PIXIVPY_REFRESH_TOKEN'))
    
    return pixivpy