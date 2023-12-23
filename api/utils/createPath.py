import os
scriptDir = os.path.dirname(os.path.abspath(__file__))
def createPath(*paths):
    return os.path.join(scriptDir, *paths)