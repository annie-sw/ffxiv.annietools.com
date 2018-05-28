<template>
  <div id="app" v-if="initialized">
    <nav>
      <router-link to="/">Index</router-link>
      <router-link to="/WeatherForecast">WeatherForecast</router-link>
      <router-link to="/Timeline">Timeline</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
import api from '@/api'

const loadData = async (completed, receivedData, receivedText) => {
  if (!receivedData) {
    let {data, error} = await api.bin.get('/static/data/data')
    if (!error) {
      receivedData = data
    }
  }
  if (!receivedText) {
    let {data, error} = await api.bin.get('/static/data/text')
    if (!error) {
      receivedText = data
    }
  }
  if (receivedData && receivedText) {
    completed(receivedData, receivedText)
  } else {
    await loadData(completed, receivedData, receivedText)
  }
}

export default {
  name: 'App',

  data () {
    return {
      initialized: false
    }
  },

  async beforeCreate () {
    await loadData((data, text) => {
      this.$store.commit('General/setData', { data, text })
      this.initialized = true
    })
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
