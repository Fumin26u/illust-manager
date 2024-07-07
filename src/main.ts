import { createApp } from 'vue'
import { createPinia } from 'pinia'

import { useUserStore } from '@/store/userStore'

import App from './App.vue'
import router from './router'
import vuetify from '../plugins/vuetify'

const app = createApp(App)
app.use(router)
app.use(createPinia())

const userStore = useUserStore()
// アプリケーションの起動
const initApp = async () => {
    await userStore.getUser()
    app.use(vuetify).mount('#app')
}

initApp()
