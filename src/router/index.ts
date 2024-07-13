import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import imagedler from '../views/imagedler.vue'
import user from '../views/user.vue'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'user',
        component: user,
    },
    {
        path: '/imagedler',
        name: 'imagedler',
        component: imagedler,
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})

export default router
