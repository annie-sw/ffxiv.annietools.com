<template>
  <div v-if="eorzeaTime">
    <h1>Weather Forecast</h1>
    <div>
      <span> ET: {{ formatTime(eorzeaTime) }} </span>
      <span> {{ lib.getMoonName(eorzeaTime.moon) }} </span>
    </div>
    <div>
      <span v-for="regionId in regionIds"
            v-on:click="onSelectedRegion(regionId)"
            v-bind:key="'region:' + regionId">
        {{ lib.getPlaceName(regionId) }}
      </span>
    </div>
    <div>
      <span v-for="weatherId in weatherIds"
            v-bind:style="selectedWeathers.indexOf(weatherId) >= 0 && {'color':'orange'}"
            v-on:click="onSelectedWeather(weatherId)"
            v-bind:key="'weather-selector:' + weatherId">
        {{ lib.getWeatherName(weatherId) }}
      </span>
    </div>
    <div>
      <div v-for="(rateId, placeId) in selectedPlaces"
           v-bind:key="'place:' + placeId">
        {{ lib.getPlaceName(placeId) }}
        <div v-for="weather in weathers[rateId]"
             v-bind:key="'weather:' + placeId + '-' + weather.time.et.totalSeconds">
          <span> ET: {{ formatTime(weather.time.et) }} </span>
          <span> Weather: {{ lib.getWeatherName(weather.weatherId) }} </span>
          <span> LT: {{ formatDate(weather.time.lt) }} {{ formatTime(weather.time.lt) }} </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import WeatherForecast from '@/scripts/libWeatherForecast'

export default {
  // name: 'HelloWorld',
  data () {
    return {
      timeId: 0,
      regionIds: [],
      selectedPlaces: {},
      selectedWeathers: [],
      eorzeaTime: null,
      startWeatherTime: 0
    }
  },
  computed: {
    lib () {
      return WeatherForecast
    },
    weatherIds () {
      /**
       * 天候リストを作成
       * data:{selectedPlaces} に依存
       */
      return WeatherForecast.getWeathers(Object.values(this.selectedPlaces))
    },
    weathers () {
      /**
       * エリア毎の天候タイムラインを作成
       * data:{startWeatherTime, selectedWeathers} に依存
       * computed:{weatherIds} に依存
       */
      const nums = 432 // 地球時間の一週間分
      const max = 3 * 8 // エオルゼア時間の一週間分

      const weathers = {}
      const weatherTimes = WeatherForecast.getWeatherTimes(this.startWeatherTime, nums)

      for (const rateId of new Set(Object.values(this.selectedPlaces))) {
        const w = weathers[rateId] = []
        for (const time of weatherTimes) {
          const weatherId = WeatherForecast.getWeatherId(time.et.totalSeconds, rateId)
          if (this.selectedWeathers.length === 0 || this.selectedWeathers.indexOf(weatherId) >= 0) {
            if (w.push({ time: time, weatherId: weatherId }) >= max) {
              break
            }
          }
        }
      }
      return weathers
    }
  },
  mounted () {
    WeatherForecast.setData(this.$store.state.General.data, this.$store.state.General.text)
    const frameTick = () => {
      // 現在のエオルゼア時間を取得
      const eorzeaTimeSec = WeatherForecast.convertToEorzeaTime(new Date().getTime() / 1000)
      const newMinutes = (eorzeaTimeSec / WeatherForecast.MINUTE_SPAN) >>> 0
      const oldMinutes = (((!!this.eorzeaTime && this.eorzeaTime.totalSeconds) || 0) / WeatherForecast.MINUTE_SPAN) >>> 0
      if (newMinutes !== oldMinutes) {
        // エオルゼア時間の分が変わっていたら更新
        this.eorzeaTime = WeatherForecast.getEorzeaTime(eorzeaTimeSec)

        const nowWeatherTime = WeatherForecast.resolveWeatherTime(eorzeaTimeSec)
        if (this.startWeatherTime !== nowWeatherTime) {
          // 天候変更時間が変わっていたら更新
          this.startWeatherTime = nowWeatherTime
        }
      }
    }
    this.regionIds = WeatherForecast.getRegions()
    this.selectedPlaces = WeatherForecast.getPlaces(this.regionIds[0])
    frameTick()
    this.timeId = setInterval(frameTick, 300)
  },
  beforeDestroy () {
    clearInterval(this.timeId)
  },
  methods: {
    formatDate (t) {
      return (t.month < 10 ? '0' : '') + t.month + '-' + (t.day < 10 ? '0' : '') + t.day
    },
    formatTime (t) {
      return (t.hours < 10 ? '0' : '') + t.hours + ':' + (t.minutes < 10 ? '0' : '') + t.minutes
    },
    onSelectedRegion (regionId) {
      this.selectedPlaces = WeatherForecast.getPlaces(regionId)
      this.selectedWeathers = []
    },
    onSelectedWeather (weatherId) {
      const index = this.selectedWeathers.indexOf(weatherId)
      if (index >= 0) {
        this.selectedWeathers.splice(index, 1)
      } else {
        this.selectedWeathers.push(weatherId)
      }
    }
  }
}
</script>

<style scoped>
</style>
