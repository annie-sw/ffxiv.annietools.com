import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/pages/Index'
import MiniCactpot from '@/pages/MiniCactpot/MiniCactpot'
import WeatherForecast from '@/pages/WeatherForecast'
// import Timeline from '@/pages/Timeline'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/WeatherForecast',
      name: 'WeatherForecast',
      component: WeatherForecast
    },
    {
      path: '/MiniCactpot',
      name: 'MiniCactpot',
      component: MiniCactpot
    }
  ]
})
