from datetime import datetime
def getNowTime():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")