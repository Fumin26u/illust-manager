// blobの画像リンクをBASE64に変換
export const convertImageToBase64 = async (image: string) => {
    try {
        const response = await fetch(image)
        const blob = await response.blob()
        const base64 = await new Promise((resolve, reject) => {
            const reader = new FileReader()
            reader.onload = () => resolve(reader.result)
            reader.onerror = () => reject(null)
            reader.readAsDataURL(blob)
        })
        return base64
    } catch (error) {
        console.error(error)
    }
}
