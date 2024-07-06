import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import twitter from '../views/twitter.vue'
import pixiv from '../views/pixiv.vue'
import user from '../views/user.vue'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'user',
        component: user,
    },
    {
        path: '/twitter',
        name: 'twitter',
        component: twitter,
    },
    {
        path: '/pixiv',
        name: 'pixiv',
        component: pixiv,
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})

export default router
