import cv2, os
import numpy as np
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing import image
from api.evaluate.getFace import loadImage, detectFace, saveFace, resizeImage
from api.evaluate.detect_anime_face import getFaceRect, load_checkpoint
BASE_PATH = ''

from api.evaluate.cfg import TRAIN_MODEL_PATH

# 画像がどのキャラ(クラス)に近いか分析
def analyzeImage(model, imagePath):
    img = image.load_img(imagePath, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0 
    return model.predict(img_array)

# 分析結果と一致度の表示
def displayAnalyzeResult(predictions, generator):    
    classLabels = list(generator.class_indices.keys())  # クラスのラベル
    
    classPredictions = [
        {'className': label, 'probability': predictions[0][i]} for i, label in enumerate(classLabels)
    ]
    
    sorted_predictions = sorted(classPredictions, key=lambda x: x['probability'], reverse=True)
    for prediction in sorted_predictions:
        prediction['probability'] = format(prediction['probability'], '.4f')  # 小数第4位まで表示
        prediction['probability'] = f"{float(prediction['probability']) * 100:.2f}%"  # パーセンテージ表記
    
    return sorted_predictions

# 画像の削除
def deleteImage(imagePath):
    try:
        os.remove(imagePath)
    except FileNotFoundError:
        pass

# 全体の実行
def main(
    evaluatedImage, 
    croppedImagePath, 
    trainExtends,
    modelPath = TRAIN_MODEL_PATH, 
    base_path = BASE_PATH
):
    # モデルのロード
    model = load_model(modelPath) 

    # 前回の評価画像・リサイズ画像が残っていれば削除
    deleteImage(croppedImagePath)
    
    # 画像の顔部分を切り抜き保存 + 保存先のパス取得
    image = resizeImage(evaluatedImage, 1280)
    
    faceRect = getFaceRect(image)
    # 顔認識がなされなかった場合、各クラス＋othersを設定し、othersを100%にする
    if len(faceRect) == 0:
        print(evaluatedImage)
        return [
            {'className': 'others', 'probability': '100.00%'},    
        ] + [
            {'className': label, 'probability': '0.00%'} for label in list(trainExtends.class_indices.keys())
        ]

    saveFace([faceRect[0]], image, base_path, croppedImagePath, (224, 224))

    # モデルの分析
    predictions = analyzeImage(model, croppedImagePath)

    # 結果表示
    return displayAnalyzeResult(predictions, trainExtends)