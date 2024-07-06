import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import evaluate from '../../backup/evaluate.vue'
import twitter from '../views/twitter.vue'
import pixiv from '../views/pixiv.vue'
import account from '../views/account.vue'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'index',
        component: evaluate,
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
    {
        path: '/account',
        name: 'account',
        component: account,
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})

export default router
