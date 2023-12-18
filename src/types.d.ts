export interface ImageInfo {
    rawPath: string
    imagePath: string
    className: string
    confidence: string | undefined
    isImportant: boolean
    index: number
}

export interface EvaluatedResult {
    className: string
    probability: string
}
