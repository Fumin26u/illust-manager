export interface Image {
    id: string
    url: string
    selected: boolean
}

export interface Post {
    id: string
    created_at?: string
    user: string
    text: string
    images: Image[]
    url: string
}
