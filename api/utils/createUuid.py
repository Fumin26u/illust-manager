import uuid
def createUuid(length):
    return str(uuid.uuid4())[:length]