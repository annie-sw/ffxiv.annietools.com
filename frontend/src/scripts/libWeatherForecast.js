let DATA = null
let TEXT = null

export default {
  MOON_SPAN: 86400 * 4,
  WEATHER_SPAN: 3600 * 8,
  YEAR_SPAN: 86400 * 384,
  MONTH_SPAN: 86400 * 32,
  WEEK_SPAN: 86400 * 8,
  DAY_SPAN: 86400,
  // DAY_QUARTER_SPAN: 3600 * 6,
  HOUR_SPAN: 3600,
  MINUTE_SPAN: 60,

  setData (_, __) {
    DATA = _
    TEXT = __
  },
  convertToEorzeaTime (unixSec) {
    // UNIX時間をエオルゼア時間に変換 (秒)
    return unixSec * (1440.0 / 70.0)
  },
  convertToUnixTime (eorzeaSec) {
    // エオルゼア時間をUNIX時間に変換 (秒)
    return eorzeaSec * (70.0 / 1440.0)
  },
  getEorzeaTime (eorzeaTimeSec) {
    // エオルゼア時間オブジェクト
    const t = eorzeaTimeSec
    const hours = parseInt((t / this.HOUR_SPAN) % 24)
    return {
      moon: parseInt(t / this.MOON_SPAN) % 8,
      year: parseInt(t / this.YEAR_SPAN) + 1,
      month: parseInt((t / this.MONTH_SPAN) % 32) + 1,
      day: parseInt((t / this.DAY_SPAN) % 32) + 1,
      week: parseInt((t / this.WEEK_SPAN) % 8),
      hours_quorter: parseInt((t / this.HOUR_SPAN) % 4),
      hours: hours,
      hour_attr: parseInt(hours % 6),
      minutes: parseInt((t / this.MINUTE_SPAN) % 60),
      seconds: parseInt(t % 60),
      totalSeconds: t
    }
  },
  getLocalTime (eorzeaTimeSec) {
    // ローカル時間オブジェクト
    const date = new Date(this.convertToUnixTime(eorzeaTimeSec) * 1000)
    return {
      year: date.getYear(),
      month: date.getMonth() + 1,
      day: date.getDate(),
      week: date.getDay(),
      hours: date.getHours(),
      minutes: date.getMinutes(),
      seconds: date.getSeconds(),
      totalSeconds: date.getTime() / 1000
    }
  },

  getPlaceName (nameId) {
    // エリア名を取得
    return TEXT.placeNames(nameId)
  },
  getWeatherName (nameId) {
    // 天候名を取得
    return TEXT.weatherNames(nameId)
  },
  getMoonName (nameId) {
    // 月齢の名前を取得
    const names = ['新月', '三日月', '上弦の月', '十三夜', '満月', '十六夜', '下弦の月', '二十六夜']
    return names[nameId]
  },

  getRegions () {
    // リージョンリストを取得
    const mapLength = DATA.weatherMapsLength()
    const regions = []
    for (let i = 0; i < mapLength; ++i) {
      const map = DATA.weatherMaps(i)
      const region = map.region()
      if (regions.indexOf(region) < 0) {
        regions.push(region)
      }
    }
    return regions
    // return regions.sort((a, b) => a - b)
  },
  getPlaces (regionId) {
    // エリアリストを取得
    const mapLength = DATA.weatherMapsLength()
    const places = {}
    for (let i = 0; i < mapLength; ++i) {
      const map = DATA.weatherMaps(i)
      if (regionId === map.region()) {
        const place = map.place()
        const rate = map.rate()
        places[place] = rate
      }
    }
    return places
  },
  getWeathers (weatherRates) {
    // 天候リストを取得
    if (!weatherRates || weatherRates.length === 0) {
      const weathers = Array(TEXT.weatherNamesLength())
      for (let i = 0; i < weathers.length; ++i) {
        weathers[i] = i
      }
      return weathers
    }
    let weathers = []
    for (const rate of weatherRates) {
      Array.prototype.push.apply(weathers, rate.weathersArray())
    }
    // return [...new Set(weathers)].sort((a, b) => a - b)
    return [...new Set(weathers)]
  },

  resolveWeatherTime (eorzeaTimeSec) {
    // 天候変更時間を取得
    return parseInt(eorzeaTimeSec - (eorzeaTimeSec % this.WEATHER_SPAN))
  },
  getWeatherTimes (startTime, nums) {
    // 天候変更時間のリストを取得
    const times = Array(nums)
    for (let i = 0; i < nums; ++i) {
      const t = startTime + this.WEATHER_SPAN * i
      times[i] = {
        et: this.getEorzeaTime(t),
        lt: this.getLocalTime(t)
      }
    }
    return times
  },
  getWeatherId (eorzeaTimeSec, weatherRate) {
    // 天候を取得
    const wt = eorzeaTimeSec
    const days = parseInt(wt / this.DAY_SPAN)
    const hour = parseInt(wt / this.HOUR_SPAN) % 24
    const base = (days * 100) + ((hour + 8) % 24)
    const step1 = ((base << 11) ^ base) & 0xffffffff
    const step2 = ((step1 >> 8) ^ step1) & 0xffffffff
    const rate = step2 % 100

    const length = weatherRate.ratesLength()
    let threshold = 0
    for (let n = 0; n < length; ++n) {
      threshold += weatherRate.rates(n)
      if (rate < threshold) {
        return weatherRate.weathers(n)
      }
    }
    return 0
  }
}
