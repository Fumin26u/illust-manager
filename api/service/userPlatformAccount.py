from api.model import db, UserPlatformAccount

def select(user_id, platform):
    return (
        UserPlatformAccount.query
            .filter_by(
                user_id = user_id, 
                platform = platform
            )
            .first()
            .to_dict()
    )
    
def update(userPlatformAccountId, args):
    print(args)
    (db.session
        .query(UserPlatformAccount)
        .filter_by(id = userPlatformAccountId)
        .update(args)
    )