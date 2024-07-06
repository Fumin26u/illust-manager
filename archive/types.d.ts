/* -----------------  

    画像評価関連

----------------- */

export interface EvaluatedResult {
    className: string
    probability: string
}

export interface ImageInfo {
    rawPath: string
    imagePath: string
    childDir: string
    classList?: EvaluatedResult[]
    className: string
    probability?: string
    isImportant: boolean
    index: number
}

/* -----------------  

    モデル訓練関連

----------------- */
// 活性関数
export type Activation =
    | 'relu'
    | 'sigmoid'
    | 'softmax'
    | 'softplus'
    | 'softsign'
    | 'tanh'
    | 'selu'
    | 'elu'
    | 'exponential'
    | 'linear'

export type Padding = 'valid' | 'same' | 'causal'

export type Optimizer =
    | 'adam'
    | 'sgd'
    | 'rmsprop'
    | 'adagrad'
    | 'adadelta'
    | 'adamax'
    | 'nadam'

// ImageDataGenerator Class
export interface ImageDataGenerator {
    rescale: number
    shear_range: float
    zoom_range: float
    horizontal_flip: boolean
    validation_split: float
}

// ImageDataGenerator.flow_from_directory()
export interface TrainFlows {
    resize_resolution: [number, number]
    batch_size: number
    class_mode: string
}

// 畳み込み層(Conv2D)
export interface Conv2d {
    filters: number
    kernel_size: [number, number]
    activation: Activation
    input_shape: [number, number, number]
    padding?: Padding
    strides?: [number, number]
    use_bias?: boolean
}

// プーリング層(MaxPooling2D)
export interface MaxPooling2d {
    pool_size: [number, number]
    strides?: [number, number]
    padding?: Padding
}

// 畳み込み層・プーリング層・ドロップアウト層の組み合わせ(CNN)
export interface CNN {
    uuid: string
    conv2d: Conv2d
    maxPooling2d: MaxPooling2d
    dropout: float
}

// 結合層(Dense)
export interface Dense {
    uuid: string
    units: 'class_length' | number
    activation: Activation
    isUsingClassLength: boolean
}

// EarlyStopping
export interface EarlyStopping {
    monitor: string
    patience: number
    verbose: number
    mode: string
    restore_best_weights: boolean
}

// モデル構築全体
export interface TrainModels {
    batchNormalization: boolean
    flatten: boolean
    cnn: CNN[]
    dense: Dense[]
    final_dropout: float
}

// データセットの処理関連
export interface DataSets {
    imageDataGenerator: ImageDataGenerator
    trainFlows: TrainFlows
}

// 訓練全体
export interface TrainParameters {
    isSetEarlyStopping: boolean
    earlyStopping: EarlyStopping
    optimizer: string
    epochs: number
}