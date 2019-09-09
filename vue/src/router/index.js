import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    name: '404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/empty',
    name: 'empty',
    component: () => import('@/views/empty'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '控制台', icon: 'dashboard' }
    }]
  },

  {
    path: '/account',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'account',
        component: () => import('@/views/account/index'),
        meta: { title: '账 户', icon: 'user' }
      }
    ]
  },

  {
    path: '/quotation',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'quotation',
        component: () => import('@/views/quotation/index'),
        meta: { title: '行 情', icon: '行情' }
      }
    ]
  },
  {
    path: '/editor',
    component: Layout,
    hidden: true,
    children: [
      {
        path: 'index',
        name: 'editor',
        component: () => import('@/views/editor/index'),
        meta: { title: '编辑器', icon: '策略' }
      }
    ]
  },
  {
    path: '/strategy',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'strategy',
        component: () => import('@/views/strategy/index'),
        meta: { title: '策 略', icon: '策略' }
      }
    ]
  },

  {
    path: '/retreat',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'retreat',
        component: () => import('@/views/retreat/index'),
        meta: { title: '回 测', icon: '回撤' }
      }
    ]
  },
  {
    path: '/order',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'order',
        component: () => import('@/views/order/index'),
        meta: { title: '下 单', icon: '下单' }
      }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}
export default router
