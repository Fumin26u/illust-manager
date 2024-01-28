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

/* -----------------  

    アカウント関連

----------------- */
export interface UserInfo {
    created_at: string
    updated_at: string
    dl_count: number
    images_count: number
    pixiv: UserPixivInfo[]
    twitter: UserTwitterInfo[]
    twitter_password: string
    user_name: string
}

export interface UserPixivInfo {
    id: string
    post: string
    tag: string
}

export interface UserTwitterInfo {
    id: string
    post: string
}

/* -----------------  

    ImageDLer

----------------- */
// Twitter
export interface TwiSearch {
    twitterID: string
    getTweetType: 'liked_tweets' | 'tweets' | 'bookmarks'
    getNumberOfTweet: string
    isGetFromPreviousTweet: boolean
    suspendID: string
}

export interface TweetImage {
    id: string
    url: string
    selected: boolean
}

export interface TweetInfo {
    postID: string
    post_time: boolean
    user: string
    text: string
    images: TweetImage[]
    url: string
}

// pixiv
export interface PixSearch {
    userID: number
    tag: string
    getPostType: 'bookmark' | 'post' | 'tag'
    getNumberOfPost: string
    minBookmarks: number
    isGetFromPreviousPost: boolean
    includeTags: boolean
    suspendID: string
    isIgnoreSensitive: boolean
}

export interface PixPostInfo {
    postID: string
    post_time: boolean
    user: string
    text: string
    images: TweetImage[]
    url: string
}

export interface PixPostImage {
    id: string
    url: string
    selected: boolean
}
