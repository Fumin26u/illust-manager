// Python API Path
const apiOrigin = 'http://127.0.0.1:5000'
export const createEndPoint = (path: string) => {
    return `${apiOrigin}${path}`
}
