const List = () => import(/* webpackChunkName: "trip" */ '@/views/trip/List.vue')

export default {
  path: '/trip',
  component: { template: '<router-view />' },
  children: [
    {
      path: '',
      name: 'Trip',
      component: List
    }
  ]
}
