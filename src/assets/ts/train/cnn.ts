import { CNN, Conv2d, MaxPooling2d } from '@/types/types'
import { ref } from 'vue'

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

export const createCnnInit = (): CNN => {
    return {
        conv2d: {
            filters: 32,
            kernel_size: [3, 3],
            activation: 'relu',
            input_shape: [224, 224, 3],
        },
        maxPooling2d: {
            pool_size: [2, 2],
        },
        dropout: 0.05,
        uuid: '',
    }
}
