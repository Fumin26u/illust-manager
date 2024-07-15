from api.model import db, UserPlatformAccountDlLog
    
def select(userPlatformAccountId, limit = 200):
    return (
        UserPlatformAccountDlLog.query
            .with_entities(UserPlatformAccountDlLog.post_id)
            .filter_by(user_platform_account_id = userPlatformAccountId)
            .order_by(UserPlatformAccountDlLog.downloaded_at.desc())
            .limit(limit)
            .all()
    )
    
def create(userPlatformAccountId, postId, downloadedAt):
    db.session.add(
        UserPlatformAccountDlLog(
            user_platform_account_id = userPlatformAccountId,
            post_id = postId,
            downloaded_at = downloadedAt
        )
    )