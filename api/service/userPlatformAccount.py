import api.model.UserPlatformAccount

def select(user_id, platform):
    return api.model.UserPlatformAccount.select(user_id, platform)
    
def update(userPlatformAccountId, args):
    return api.model.UserPlatformAccount.update(userPlatformAccountId, args)