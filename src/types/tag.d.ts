export interface Tag {
    selected: boolean
    id: number
    name_en: string
    name_ja: string
    post_count: number
    category_id: number
    is_deprecated: boolean
    created_at: string
    updated_at: string
    words: TagWord[]
}

export interface TagWord {
    id: number
    tag_id?: number
    name_en: string
    name_ja?: string
}

export interface Category {
    id: number
    name_en: string
    name_ja?: string
    is_deprecated: boolean
}

export interface CategoryMaster {
    id: string
    name_en: string
    name_ja?: string
}
