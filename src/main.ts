import { createApp } from 'vue'
import { createPinia } from 'pinia'

import { useAccountStore } from '@/store/userStore'
import { getUserInfo } from '@/assets/ts/getUserInfo'

import App from './App.vue'
import router from './router'
import vuetify from '../plugins/vuetify'

const app = createApp(App)
app.use(router)
app.use(createPinia())

const accountStore = useAccountStore()
// アプリケーションの起動
const initApp = async () => {
    accountStore.$patch({
        userInfo: await getUserInfo(),
    })
    app.use(vuetify).mount('#app')
}

initApp()
