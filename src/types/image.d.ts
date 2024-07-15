export interface ImageTag {
    id: number
    user_image_id: number
    name_en: string
    name_ja: string
}

export interface RawImage {
    id?: number
    name: string
    path: string
    tags?: ImageTag[]
    image?: any
    created_at?: string
    updated_at?: string
}

export interface Image {
    id: number
    user_id: number
    name: string
    tags: ImageTag[]
    image?: any
    created_at: Date
    updated_at: Date
}
