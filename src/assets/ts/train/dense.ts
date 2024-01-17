import { Dense } from '@/types'

export const activations = [
    'relu',
    'sigmoid',
    'softmax',
    'softplus',
    'softsign',
    'tanh',
    'selu',
    'elu',
    'exponential',
    'linear',
]

export const createDenseInit = (): Dense => {
    return {
        units: 128,
        activation: 'softmax',
        uuid: '',
        isUsingClassLength: true,
    }
}
