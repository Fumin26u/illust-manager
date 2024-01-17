from flask import Blueprint, request, jsonify

from api.utils.createPath import createPath
from api.utils.getNowTime import getNowTime
from api.utils.createTrainData import createTrainData
from api.train.train import createTrainedModel

trainRoutes = Blueprint('trainRoutes', __name__)


@trainRoutes.route('/train/train', methods=['POST'])
def train():
    data = request.get_json()
    # 使用するデータセットのパス
    path = data.get('path', '')
    referencePath = createPath('save', 'face_images', path)
    
    # 詳細設定の存在可否
    isSetDetail = data.get('isSetDetail', False)
    # データ拡張時のパラメータ
    dataset = data.get('dataset', False) 
    # モデル構築時のパラメータ
    train_model = data.get('train_model', False)
    # 訓練実行時のパラメータ
    train_parameter = data.get('train_parameter', False)
    
    try:
        referencePath = createPath('save', 'face_images', path)
        
        nowTime = getNowTime()
        # 各種パラメータをテキストに保存
        txtPath = createPath('save', 'train_texts', f'train-{nowTime}.txt')
        with open(txtPath, "w") as file:
            file.write(f"path: {path}\n")
            file.write(f"referencePath: {referencePath}\n")
            file.write(f"isSetDetail: {isSetDetail}\n")
            file.write(f"dataset: {dataset}\n")
            file.write(f"train_model: {train_model}\n")
            file.write(f"train_parameter: {train_parameter}\n")
        
        # データ拡張
        if isSetDetail:
            imageDataGenerator = dataset['imageDataGenerator']
            flowFromDirectory = dataset['trainFlows']
            extendImages, validationImages = createTrainData(
                referencePath, 
                imageDataGenerator, 
                flowFromDirectory
            )
        else:
            extendImages, validationImages = createTrainData(referencePath)
        
        savePath = createPath('save', 'train_face_models', f'model-{nowTime}.h5')
        
        # モデル構築＋訓練
        createTrainedModel(
            extendImages, 
            validationImages, 
            referencePath, 
            savePath, 
            train_parameter,
            isSetDetail,
            train_model,
        )
        
        return jsonify({'error': False, 'content': f'success, save path: {savePath}'})
    except Exception as e:
        print(f"Error training model: {str(e)}")
        return jsonify({'error': True, 'content': {str(e)}})