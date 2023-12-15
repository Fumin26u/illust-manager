import cv2, os
import numpy as np
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing import image
from getFace import loadImage, detectFace, saveFace, resizeImage
from detect_anime_face import getFaceRect
BASE_PATH = './'

from cfg import IMAGE_MODEL_PATH, EVALUATED_IMAGE_PATH, CROPPED_IMAGE_PATH, TRAIN_MODEL_PATH
from train import trainExtends

# 画像がどのキャラ(クラス)に近いか分析
def analyzeImage(model, imagePath):
    img = image.load_img(imagePath, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0 
    return model.predict(img_array)

# 分析結果と一致度の表示
def displayAnalyzeResult(predictions, generator):
    classLabels = list(generator.class_indices.keys())  # クラスのラベル
    predictedClass = np.argmax(predictions)  # 予測されたクラス
    confidence = predictions[0][predictedClass]  # 一致度

    print(f"Predicted Class: {classLabels[predictedClass]}")
    print(f"Confidence: {confidence}")

# 画像の削除
def deleteImage(imagePath):
    try:
        os.remove(imagePath)
    except FileNotFoundError:
        pass

# 全体の実行
def main(modelPath = TRAIN_MODEL_PATH):
    # モデルのロード
    model = load_model(modelPath) 

    # 前回の評価画像・リサイズ画像が残っていれば削除
    deleteImage(CROPPED_IMAGE_PATH)

    # 画像の顔部分を切り抜き保存 + 保存先のパス取得
    image = resizeImage(loadImage(EVALUATED_IMAGE_PATH), 1280)
    faceRect = getFaceRect(image)
    saveFace([faceRect[0]], image, BASE_PATH, CROPPED_IMAGE_PATH, (224, 224))

    # モデルの分析
    predictions = analyzeImage(model, CROPPED_IMAGE_PATH)

    # 結果表示
    displayAnalyzeResult(predictions, trainExtends)

main(TRAIN_MODEL_PATH)