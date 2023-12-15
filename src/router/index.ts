import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import index from '../views/index.vue'
import training from '../views/training.vue'
import evaluate from '../views/evaluate.vue'

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
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})

export default router
