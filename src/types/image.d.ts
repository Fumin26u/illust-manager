export interface Directory {
    name: string
    count: number
}

export interface ImageTag {
    id: number
    user_image_id: number
    tag_id: number
}

export interface RawImage {
    id?: number
    name: string
    path: string
    platform?: string
    directory?: string
    imported_path?: string
    base64?: string | unknown
    tags?: ImageTag[]
    created_at?: string
    updated_at?: string
}

export interface Image {
    id?: number
    user_id: number
    directory: string
    name: string
    tags: ImageTag[]
    base64?: string | unknown
    delete_fg?: boolean
    created_at: Date
    updated_at: Date
}
