import { ref } from 'vue'

const optimizers = ref<string[]>([
    'SGD',
    'Momentum',
    'Adam',
    'Adagrad',
    'Adadelta',
    'Adamax',
    'RMSProp',
])

export default optimizers
