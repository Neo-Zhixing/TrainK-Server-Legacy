const App = () => import(/* webpackChunkName: "user" */ '@/views/user/App')
const Account = () => import(/* webpackChunkName: "user" */ '@/views/user/Account')
const Security = () => import(/* webpackChunkName: "user" */ '@/views/user/Security')
const CR12306 = () => import(/* webpackChunkName: "user" */ '@/views/user/CR12306')
const Passenger = () => import(/* webpackChunkName: "user" */ '@/views/user/Passenger')
export default {
  path: '/user/setting',
  component: App,
  children: [
    {
      path: '',
      name: 'User-Setting',
      redirect: 'account'
    },
    {
      path: 'account',
      name: 'User-Setting-Account',
      component: Account
    },
    {
      path: 'security',
      name: 'User-Setting-Security',
      component: Security
    },
    {
      path: '12306',
      name: 'User-Setting-CR12306',
      component: CR12306
    },
    {
      path: 'passenger',
      name: 'User-Setting-Passenger',
      component: Passenger
    }
  ]
}
