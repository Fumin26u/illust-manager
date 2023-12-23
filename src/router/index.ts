import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import crop from '../views/crop.vue'
import training from '../views/training.vue'
import evaluate from '../views/evaluate.vue'
import twitter from '../views/twitter.vue'
import pixiv from '../views/pixiv.vue'

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
        path: '/training',
        name: 'training',
        component: training,
    },
    {
        path: '/evaluate',
        name: 'evaluate',
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
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})

export default router
