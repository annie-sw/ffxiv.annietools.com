import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import WeatherForecast from '@/components/WeatherForecast'
import Timeline from '@/components/Timeline'

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
      path: '/Timeline',
      name: 'Timeline',
      component: Timeline
    }
  ]
})
