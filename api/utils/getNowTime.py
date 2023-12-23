from datetime import datetime
def getNowTime():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")