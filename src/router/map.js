const App = () => import(/* webpackChunkName: "map" */ '@/map/App')
export default {
  path: '/map',
  name: 'Map',
  component: App
}
