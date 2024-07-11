import os
from flask import make_response
from api.utils.string import getRootDir

def downloadZip(timestamp, platform):
    response = make_response
    zipPath = f"{getRootDir}/downloads/{platform}/zip/{timestamp}.zip"
    
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(zipPath)}'
    response.data = open(zipPath, 'rb').read()
    
    return response