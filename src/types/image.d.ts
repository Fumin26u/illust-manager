export interface Directory {
    name: string
    count: number
}

export interface ImageTag {
    id: number
    user_image_id: number
    tag_id: number
    checked: boolean
}

export interface Tag {
    name_en: string
    confidence: string
    is_saved: boolean
}

export interface Image {
    id?: number
    name: string
    path: string
    platform?: string
    directory?: string
    imported_path?: string
    base64?: string | unknown
    tags?: Tag[]
    user_id?: number
    delete_fg?: boolean
    created_at?: string
    updated_at?: string
}
