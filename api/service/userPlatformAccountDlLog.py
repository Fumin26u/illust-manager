from api.model import db, UserPlatformAccountDlLog
from sqlalchemy.sql import func
    
def select(userPlatformAccountId, limit = 100):
    subquery = (
        db.session.query(func.max(UserPlatformAccountDlLog.downloaded_at))
        .filter_by(user_platform_account_id=userPlatformAccountId)
        .scalar_subquery()
    )
    return (
        UserPlatformAccountDlLog.query
            .with_entities(UserPlatformAccountDlLog.post_id)
            .filter_by(user_platform_account_id = userPlatformAccountId)
            .filter(UserPlatformAccountDlLog.downloaded_at == subquery)
            .order_by(UserPlatformAccountDlLog.downloaded_at.desc())
            .limit(limit)
            .all()
    )
    
def create(userPlatformAccountId, postId, downloadedAt):
    print(userPlatformAccountId, postId, downloadedAt)
    db.session.add(
        UserPlatformAccountDlLog(
            user_platform_account_id = userPlatformAccountId,
            post_id = postId,
            downloaded_at = downloadedAt
        )
    )