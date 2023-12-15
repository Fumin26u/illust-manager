import getFace
import os
BASE_PATH = './'

from cfg import RAW_PATH, SAVE_PATH, RESIZE_RESOLUTION

# rawdata/ 以下のディレクトリ名
dirs = ['ayaka', 'barbara', 'furina', 'ganyu', 'hutao', 'keqing', 'kokomi', 'lumine', 'nilou']
if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)
for dir in dirs:
    print(f'Processing {dir}...')
    if not os.path.exists(f'{SAVE_PATH}{dir}'):
        os.mkdir(f'{SAVE_PATH}{dir}')
    getFace.clipImageToFace(f'{RAW_PATH}{dir}/', f'{SAVE_PATH}{dir}/', RESIZE_RESOLUTION)
    print('------------------')