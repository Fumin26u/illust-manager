import axios from 'axios'

// インターセプターの設定
axios.interceptors.request.use(
    (config) => {
        const userId = localStorage.getItem('user_id')
        if (userId) {
            config.headers['user_id'] = userId
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

export default axios
