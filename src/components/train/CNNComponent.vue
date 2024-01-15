<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { CNN, Conv2d, MaxPooling2d } from '@/types'

const emits = defineEmits(['addCNN'])

const activations = [
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

const conv2dInit: Conv2d = {
    filters: 32,
    kernel_size: [3, 3],
    activation: 'relu',
    input_shape: [224, 224, 3],
}
const maxPooling2dInit: MaxPooling2d = {
    pool_size: [2, 2],
}

const cnnInit: CNN = {
    conv2d: conv2dInit,
    maxPooling2d: maxPooling2dInit,
    dropout: 0.05,
}

const addCNN = () => {
    emits('addCNN', cnnInit)
}

onMounted(() => {
    addCNN()
})
</script>

<template>
    <dl>
        <div>
            <dt>畳み込み層(Conv2D)</dt>
            <dd>
                <dl>
                    <div class="filters">
                        <dt>filters</dt>
                        <dd>
                            <input
                                type="number"
                                v-model="cnnInit.conv2d.filters"
                                min="16"
                                step="16"
                                max="512"
                            />
                        </dd>
                    </div>
                    <div>
                        <dt>kernel_size</dt>
                        <dd>
                            <input
                                type="number"
                                v-model="cnnInit.conv2d.kernel_size[0]"
                                min="2"
                                step="1"
                                max="8"
                            />
                            x
                            <input
                                type="number"
                                v-model="cnnInit.conv2d.kernel_size[1]"
                                min="2"
                                step="1"
                                max="8"
                            />
                        </dd>
                    </div>
                    <div>
                        <dt>activation</dt>
                        <dd>
                            <select v-model="cnnInit.conv2d.activation">
                                <option
                                    v-for="activation in activations"
                                    :key="activation"
                                >
                                    {{ activation }}
                                </option>
                            </select>
                        </dd>
                    </div>
                    <div v-if="cnnInit.conv2d.input_shape !== undefined">
                        <dt>input_shape</dt>
                        <dd>
                            <input
                                type="number"
                                v-model="cnnInit.conv2d.input_shape[0]"
                                min="120"
                                step="1"
                                max="720"
                            />
                            x
                            <input
                                type="number"
                                v-model="cnnInit.conv2d.input_shape[1]"
                                min="120"
                                step="1"
                                max="720"
                            />
                            x
                            <input
                                type="number"
                                v-model="cnnInit.conv2d.input_shape[2]"
                                min="120"
                                step="1"
                                max="720"
                            />
                        </dd>
                    </div>
                </dl>
            </dd>
        </div>
        <div>
            <dt>プーリング層(MaxPooling2d)</dt>
            <dd>
                <dl>
                    <div class="pool-size">
                        <dt>pool_size</dt>
                        <dd>
                            <input
                                type="number"
                                v-model="cnnInit.maxPooling2d.pool_size[0]"
                                min="1"
                                step="1"
                                max="12"
                            />
                            x
                            <input
                                type="number"
                                v-model="cnnInit.maxPooling2d.pool_size[1]"
                                min="1"
                                step="1"
                                max="12"
                            />
                        </dd>
                    </div>
                </dl>
            </dd>
        </div>
        <div>
            <dt>ドロップアウト</dt>
            <dd>
                <input
                    type="number"
                    v-model="cnnInit.dropout"
                    min="0"
                    step="0.05"
                    max="0.5"
                />
            </dd>
        </div>
    </dl>
</template>
