import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import index from '../views/index.vue'
import training from '../views/training.vue'
import evaluate from '../views/evaluate.vue'
import imagedler_twitter from '../views/imagedler/twitter.vue'
import imagedler_pixiv from '../views/imagedler/pixiv_new.vue'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'index',
        component: index,
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
        path: '/imagedler/twitter',
        name: 'imagedler_twitter',
        component: imagedler_twitter,
    },
    {
        path: '/imagedler/pixiv_new',
        name: 'imagedler_pixiv',
        component: imagedler_pixiv,
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})

export default router
