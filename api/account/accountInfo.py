from datetime import datetime

class AccountInfo:
    def __init__(
        self, 
        user_name, 
        created_at,
        dl_count,
        images_count,
        twitter,
        pixiv
    ):
        self.user_name = user_name
        self.created_at = created_at
        self.dl_count = dl_count
        self.images_count = images_count
        self.twitter = twitter
        self.pixiv = pixiv
        
    def toDict(self):
        return {
            'user_name': self.user_name,
            'created_at': datetime.strptime(self.created_at, '%Y-%m-%d %H:%M:%S'),
            'dl_count': self.dl_count,
            'images_count': self.images_count,
            'twitter': self.twitter,
            'pixiv': self.pixiv
        }
              
