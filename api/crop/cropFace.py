import getFace
import os, shutil
BASE_PATH = './'

# rawdata/ 以下のディレクトリ名を取得
dirs = os.listdir(RAW_PATH)
if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)
for dir in dirs:
    # ディレクトリ名を一時的に英字に変換
    raw_dir_path = os.path.join(RAW_PATH, dir)
    temp_dir_path = os.path.join(RAW_PATH, 'temp')
    
    os.rename(f'{RAW_PATH}{dir}', f'{RAW_PATH}temp')
        
    print(f'Processing {dir}...')
    if not os.path.exists(f'{SAVE_PATH}{dir}'):
        os.mkdir(f'{SAVE_PATH}temp')
    getFace.clipImageToFace(temp_dir_path, f'{SAVE_PATH}temp/', RESIZE_RESOLUTION)
    os.rename(f'{SAVE_PATH}temp', f'{SAVE_PATH}{dir}')
    
    os.rename(f'{RAW_PATH}temp', f'{RAW_PATH}{dir}')
    
    print('------------------')