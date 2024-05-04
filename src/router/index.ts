import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import crop from '../views/crop.vue'
import train from '../views/train.vue'
import evaluate from '../views/evaluate.vue'
import remove from '../views/remove.vue'
import twitter from '../views/twitter.vue'
import pixiv from '../views/pixiv.vue'
import fanbox from '../views/fanbox.vue'
import account from '../views/account.vue'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'index',
        component: evaluate,
    },
    {
        path: '/crop',
        name: 'crop',
        component: crop,
    },
    {
        path: '/train',
        name: 'train',
        component: train,
    },
    {
        path: '/evaluate',
        name: 'evaluate',
        component: evaluate,
    },
    {
        path: '/remove',
        name: 'remove',
        component: remove,
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
        path: '/fanbox',
        name: 'fanbox',
        component: fanbox,
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
