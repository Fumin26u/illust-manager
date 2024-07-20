import api.model.User

def getUser(user_id: int):
    return api.model.User.get(user_id)

def createUser(userInfo): 
    return api.model.User.create(userInfo)
    
def updateUser(user_id: int, userInfo): 
    return api.model.User.update(user_id, userInfo)