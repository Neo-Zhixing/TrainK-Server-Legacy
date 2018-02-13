const Home = () => import(/* webpackChunkName: "ticket" */ '@/views/ticket/Home')
const List = () => import(/* webpackChunkName: "ticket" */ '@/views/ticket/List')
const Order = () => import(/* webpackChunkName: "ticket" */ '@/views/ticket/Order')

export default {
  path: '/ticket',
  component: {
    template: '<router-view />'
  },
  children: [
    {
      path: '',
      name: 'Ticket-Home',
      component: Home
    },
    {
      path: 'list',
      name: 'Ticket-List',
      component: List
    },
    {
      path: 'order',
      name: 'Ticket-Order',
      component: Order
    }
  ]
}
