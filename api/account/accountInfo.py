from datetime import datetime

class AccountInfo:
    def __init__(
        self, 
        user_name, 
        created_at,
        updated_at,
        twitter_password,
        pixiv_password,
        dl_count,
        images_count,
        twitter,
        pixiv
    ):
        self.user_name = user_name
        self.created_at = created_at
        self.updated_at = updated_at
        self.twitter_password = twitter_password
        self.pixiv_password = pixiv_password
        self.dl_count = dl_count
        self.images_count = images_count
        self.twitter = twitter
        self.pixiv = pixiv
        
    def toDict(self):
        created_at = datetime.strftime(self.created_at, '%Y-%m-%d %H:%M:%S') if self.created_at != '' else ''
        updated_at = datetime.strftime(self.updated_at, '%Y-%m-%d %H:%M:%S') if self.updated_at != '' else ''
        return {
            'user_name': self.user_name,
            'created_at': created_at,
            'updated_at': updated_at,
            'twitter_password': self.twitter_password, 
            'pixiv_password': self.pixiv_password, 
            'dl_count': self.dl_count,
            'images_count': self.images_count,
            'twitter': self.twitter,
            'pixiv': self.pixiv
        }