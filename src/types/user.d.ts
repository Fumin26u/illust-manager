export interface User {
    id: number
    email: string
    user_name: string
    uuid: string
    created_at: string
    updated_at: string
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
