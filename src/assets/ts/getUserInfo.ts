import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'

const apiManager = new ApiManager()
// ユーザーデータの取得
export const getUserInfo = async () => {
    const response = await apiManager.get(`${apiPath}/api/getUserInfo`)
    return response.content.content
}
