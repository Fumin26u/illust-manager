import os
from tensorflow import keras

from keras.callbacks import EarlyStopping
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization

# モデルの構築
# デフォルトの設定
def createModel_default(extendImages):
    model = Sequential()
    model.add(BatchNormalization())
    
    model.add(Conv2D(64, (3, 3), input_shape=(224, 224, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.05))
    
    model.add(Conv2D(32, (3,3), input_shape=(224, 224, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.05))
    
    model.add(Flatten())
    # model.add(Dense(units=256, activation='relu'))
    model.add(Dense(units=128, activation='relu'))
    model.add(Dense(units=len(extendImages.class_indices), activation='softmax'))
    
    model.add(Dropout(0.05))
    
    return model

# ユーザーがフロントエンドで手動構築した場合
def createModel(extendImages, train_model):    
    model = Sequential()
    
    # cnn各層
    for layer in train_model['cnn']:
        inputShape = tuple(layer['conv2d']['input_shape'])
        kernelSize = tuple(layer['conv2d']['kernel_size'])
        
        model.add(Conv2D(
            layer['conv2d']['filters'], 
            kernelSize, 
            input_shape=inputShape, 
            activation=layer['conv2d']['activation']
        ))
        model.add(MaxPooling2D(pool_size=layer['maxPooling2d']['pool_size']))
        model.add(Dropout(layer['dropout']))
    model.add(BatchNormalization()) if train_model['batchNormalization'] else None
    
    model.add(Flatten()) if train_model['flatten'] else None
        
    # 結合層
    for layer in train_model['dense']:
        model.add(Dense(
            units=layer['units'] if not layer['isUsingClassLength'] else len(extendImages.class_indices), 
            activation=layer['activation']
        ))
        
    model.add(BatchNormalization()) if train_model['batchNormalization'] else None
    model.add(Dropout(train_model['final_dropout']))
        
    return model

# モデル作成するディレクトリから各クラスのファイル数を取得
# ファイル数を基に各クラスの重みを均一にする
def createWeights(modelDir):
    # ディレクトリ内の各サブディレクトリを取得
    subdirectories = [d for d in os.listdir(modelDir) if os.path.isdir(os.path.join(modelDir, d))]

    classWeights = dict()
    total_samples = 0

    # 各サブディレクトリ内のサンプル数を合計
    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(modelDir, subdirectory)
        files_in_subdirectory = len([f for f in os.listdir(subdirectory_path) if os.path.isfile(os.path.join(subdirectory_path, f))])
        total_samples += files_in_subdirectory

    # 各クラスの重みを計算
    for i, subdirectory in enumerate(subdirectories):
        subdirectory_path = os.path.join(modelDir, subdirectory)
        files_in_subdirectory = len([f for f in os.listdir(subdirectory_path) if os.path.isfile(os.path.join(subdirectory_path, f))])
        
        # サンプル数が0の場合に備えて、ゼロ割りエラーを防ぐ
        if files_in_subdirectory > 0:
            classWeights[i] = total_samples / (len(subdirectories) * files_in_subdirectory)
        else:
            classWeights[i] = 0

    return classWeights

# 実行
def createTrainedModel(
    extendImages, 
    validationImages, 
    faceModelPath, 
    savePath,
    train_parameter,
    isSetDetail = False,
    train_model = False,
):
    model = createModel_default(extendImages) if not isSetDetail else createModel(
        extendImages,
        train_model,
    )
    
    model.build(input_shape=(None, 224, 224, 3))
    model.summary()

    # 各クラスの重み
    classWeights = createWeights(faceModelPath)

    # コンパイル
    model.compile(
        optimizer=train_parameter['optimizer'], 
        loss='categorical_crossentropy', 
        metrics=['accuracy']
    )
    
    # EarlyStopping
    esParams = train_parameter['earlyStopping']
    early_stopping = EarlyStopping(
        monitor=esParams['monitor'], 
        patience=esParams['patience'], 
        verbose=esParams['verbose'],
        mode=esParams['mode'],
        restore_best_weights=esParams['restore_best_weights']
    )
    
    # 訓練
    model.fit(
        extendImages, 
        epochs=train_parameter['epochs'], 
        # epochs=1, 
        class_weight=classWeights,
        callbacks=[early_stopping] if train_parameter['isSetEarlyStopping'] else None,
        validation_data=validationImages
    )
    model.save(savePath)
    print(model.input_shape)  
