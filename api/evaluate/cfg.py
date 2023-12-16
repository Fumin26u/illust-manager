import os
from datetime import datetime
def getNowTime():
    return datetime.now().strftime("%Y_%m_%d_%H_%M")
BASE_PATH = 'api/evaluate/'

# 顔部分の切り抜き
# 画像フォルダのパス
IMAGE_PATH = f"{BASE_PATH}images/"
# 元データのパス
RAW_PATH = f"{IMAGE_PATH}rawdata/"
# 抜き出した顔画像の保存先
SAVE_PATH = f"{IMAGE_PATH}faces_{getNowTime()}/"
# リサイズ後の解像度
RESIZE_RESOLUTION = (224, 224)

# 訓練時のパラメータ類
# バッチサイズ
BATCH_SIZE = 32
# 学習回数
EPOCHS = 12
# ドロップアウト
DROPOUT = 0.0

# 画像の評価
# 画像モデルのパス
IMAGE_MODEL_PATH = BASE_PATH + 'opencv/lbpcascade_animeface.xml'

# 各種モデル
# 訓練に使用する顔素材のパス
FACE_MODEL_PATH = f"{IMAGE_PATH}faces_2023_12_16_18_01/"
# 評価に使用する訓練モデルのパス
TRAIN_MODEL_PATH = f"{BASE_PATH}models/model-2023-12-16-18-42-00.h5"

