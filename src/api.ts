import axios from '@/axios'

export const get = async (endPoint: string) => {
    try {
        const response = await axios.get(`${endPoint}`)
        if (response.status !== 200) {
            throw new Error('Failed to fetch')
        }

        return response.data
    } catch (error) {
        console.error(error)
    }
}

export const put = async (endPoint: string, data = {}) => {
    try {
        const response = await axios.put(`${endPoint}`, data)
        if (response.status !== 200) {
            throw new Error('Failed to update')
        }

        return response.data
    } catch (error) {
        console.error(error)
    }
}

export const post = async (endPoint: string, data = {}) => {
    try {
        const response = await axios.post(`${endPoint}`, data)
        if (response.status !== 200) {
            throw new Error('Failed to create')
        }

        return response.data
    } catch (error) {
        console.error(error)
    }
}

export const remove = async (endPoint: string) => {
    try {
        const response = await axios.delete(`${endPoint}`)
        if (response.status !== 200) {
            throw new Error('Failed to delete')
        }

        return response.data
    } catch (error) {
        console.error(error)
    }
}
