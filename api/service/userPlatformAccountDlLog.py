import api.model.UserPlatformAccountDlLog
    
def select(userPlatformAccountId, limit = 100):
    return api.model.UserPlatformAccountDlLog.select(userPlatformAccountId, limit)
    
def create(userPlatformAccountId, postId, downloadedAt):
    return api.model.UserPlatformAccountDlLog.create(userPlatformAccountId, postId, downloadedAt)