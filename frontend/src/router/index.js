import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/pages/Index'
import GatheringSpots from '@/pages/GatheringSpots'
import FishingSpots from '@/pages/FishingSpots'
import WeatherForecast from '@/pages/WeatherForecast'
import MiniCactpot from '@/pages/MiniCactpot/MiniCactpot'
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
      path: '/GatheringSpots',
      name: 'GatheringSpots',
      component: GatheringSpots
    },
    {
      path: '/FishingSpots',
      name: 'FishingSpots',
      component: FishingSpots
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
