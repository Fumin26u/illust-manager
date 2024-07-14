interface ImageTag {
    id: number
    user_image_id: number
    name_en: string
    name_ja: string
}

interface RawImage {
    id?: number
    name: string
    tags?: ImageTag[]
    created_at?: string
    updated_at?: string
}

interface Image {
    id: number
    user_id: number
    name: string
    tags: ImageTag[]
    created_at: Date
    updated_at: Date
}
