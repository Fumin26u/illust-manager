# 色々文字列生成君
import uuid, os, string, random
from datetime import datetime

# 現在時刻
def getNowTime():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# UUID
def createUuid(length):
    return str(uuid.uuid4())[:length]

# 12桁のランダム文字列
def generateRandomString(strLength: int) -> str:
    strArray = [random.choice(string.ascii_letters + string.digits) for i in range(strLength)]
    return ''.join(strArray)

# ルートディレクトリのPath
def getRootDir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))