from datetime import datetime

class AccountInfo:
    def __init__(
        self, 
        user_name, 
        created_at,
        twitter_password,
        dl_count,
        images_count,
        twitter,
        pixiv
    ):
        self.user_name = user_name
        self.created_at = created_at
        self.twitter_password = twitter_password
        self.dl_count = dl_count
        self.images_count = images_count
        self.twitter = twitter
        self.pixiv = pixiv
        
    def toDict(self):
        return {
            'user_name': self.user_name,
            'created_at': datetime.strftime(self.created_at, '%Y-%m-%d %H:%M:%S'),
            'twitter_password': self.twitter_password, 
            'dl_count': self.dl_count,
            'images_count': self.images_count,
            'twitter': self.twitter,
            'pixiv': self.pixiv
        }
              
