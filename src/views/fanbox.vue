<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'

import { ref, onMounted } from 'vue'
import ApiManager from '@/server/apiManager'
import { FanboxSearch } from '@/types'
import { apiPath } from '@/assets/ts/paths'

import '@/assets/scss/imagedler/pixForm.scss'

const search = ref<FanboxSearch>({
    userID: 'fu_min0719',
    url: '',
})

const apiManager = new ApiManager()

// 入力フォームのバリデーション
const inputValidation = (): string => {
    let error = ''
    if (search.value.userID === '') {
        error = 'ユーザーIDが入力されていません。'
    }

    if (search.value.url === '') {
        error = 'urlが入力されていません。'
    }
    return error
}

const isLoadImages = ref<boolean>(false)
const errorMessage = ref<string>('')
const imagePaths = ref<string[]>([])
const getImage = async () => {
    isLoadImages.value = true
    // 入力フォームのバリデーション
    errorMessage.value = inputValidation()
    if (errorMessage.value !== '') return

    // fanboxのユーザーまたは記事から画像URLを取得
    const response = await apiManager.post(`${apiPath}/fanbox/getImages`, {
        content: search.value,
    })

    console.log(response)
}
</script>

<template>
    <HeaderComponent />
    <main class="main-container twi-template">
        <section class="common-form">
            <dl class="form-box">
                <div>
                    <dt>ユーザーID</dt>
                    <dd>
                        <input
                            type="text"
                            id="user-id"
                            v-model="search.userID"
                        />
                    </dd>
                </div>
                <div>
                    <dt>URL(記事またはユーザー)</dt>
                    <dd>
                        <input type="text" id="url" v-model="search.url" />
                    </dd>
                </div>
                <div v-show="isLoadImages" class="btn-cover"></div>
                <ButtonComponent
                    @click="getImage()"
                    text="作品を取得"
                    :buttonClass="'btn-common green'"
                />
            </dl>
        </section>
    </main>
</template>
