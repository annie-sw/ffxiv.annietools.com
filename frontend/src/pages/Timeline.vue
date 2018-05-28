<template>
  <div>
    <span> {{ elapsedSeconds }} </span>
    <div style="border-top: 1px solid;">
      <div class="timeline-box" v-bind:style="timelineStyle">
        <div class="action"
             v-for="(action, idx) in timeline"
             v-bind:style="{top: action.top + 'px'}"
             v-bind:key="'action:' + idx">
          {{ action.text }}
        </div>
      </div>
    </div>
  </div>
</template>
<script>
const TIMELINE = [
  [
    [1, '戦闘開始'],
    [12, '中央ゴーストPOP'],
    [27, 'セイントビーム'],
    [30, '魔界の汽笛：ノックバック'],
    [37, '念力'],
    [46, '魔霊撃'],
    [56, '追突'],
    [67, '酸性雨'],
    [78, '魔界の汽笛：左右ゴースト'],
    [98, '魔界の前照灯'],
    [113, '魔界の汽笛：光で消す'],
    [133, 'セイントビーム'],
    [140, '魔界の光(MT+1)'],
    [147, '魔霊撃'],
    [148, '位置確定'],
    [154, '酸性雨'],
    [180, '雑魚POP'],
    [190, '叩きつけ'],
    [192, '範囲AoEｘ4'],
    [198, '範囲AoEｘ4']
  ],
  [
    [1, '魔界の噴煙'],
    [10, 'ゴーストPOP'],
    [11, '大：タンク'],
    [12, '小：ヒラ'],
    [13, '赤：DPS']
  ],
  [
    [1, '魔界の前照灯'],
    [1, '魔界の光(ヒラ2)'],
    [8, '位置確定'],
    [11, 'サーチライト'],
    [18, '魔霊撃'],
    [30, '魔界の汽笛：光で消す'],
    [48, 'セイントビーム'],
    [54, '魔界の汽笛：ノックバック'],
    [62, '念力'],
    [63, '魔界の前照灯'],
    [78, '追突'],
    [87, '中央ゴーストPOP'],
    [88, 'サーチライト'],
    [97, 'セイントビーム'],
    [104, '魔界の汽笛：左右ゴースト'],
    [108, '魔界の前照灯'],
    [115, '範囲AoEｘ4'],
    [121, '魔界の汽笛：光で消す'],
    [138, 'セイントビーム'],
    [141, '魔界の光(MT+1)'],
    [148, '魔霊撃'],
    [154, '酸性雨'],
    [168, '魔界の前照灯'],
    [176, '酸性雨'],
    [185, 'セイントビーム'],
    [193, '魔界の汽笛：光で消す'],
    [208, '中央ゴーストPOP'],
    [214, 'セイントビーム'],
    [215, '酸性雨'],
    [215, '魔界の光(MT+1)'],
    [222, '魔霊撃'],
    [237, '魔界の汽笛：ノックバック'],
    [245, '念力'],
    [247, '魔界の前照灯'],
    [260, '追突'],
    [271, '酸性雨'],
    [283, '中央ゴーストPOP'],
    [289, '魔界の汽笛：左右ゴースト'],
    [292, '魔界の前照灯'],
    [300, '範囲AoEｘ4'],
    [305, 'セイントビーム']
  ]
]

// const MAX_FPS = 60
const MAX_FPS = 30
const ADVANCE_TIME = 5
const ACTION_HEIGHT = 10

export default {
  data () {
    return {
      timeId: 0,
      timelineDat: TIMELINE,
      elapsedSeconds: 0,
      timeline: [],
      timeActions: {}
    }
  },
  computed: {
    timelineStyle () {
      return {
        marginTop: parseInt(this.elapsedSeconds * -ACTION_HEIGHT) + 'px'
      }
    }
  },
  mounted () {
    let timeActions = {}
    let result = []
    let totalTime = 0
    for (const phase of this.timelineDat) {
      const phaseStartTime = totalTime
      for (const t of phase) {
        const actionTime = t[0]
        const previousSpace = actionTime + phaseStartTime // - totalTime
        totalTime = phaseStartTime + actionTime
        // if (previousSpace > 0) {
        //   result.push({
        //     height: previousSpace * ACTION_HEIGHT,
        //     marginTop: 0
        //   })
        // }
        result.push({
          text: t[1],
          top: previousSpace * ACTION_HEIGHT,
          // height: 0, //ACTION_HEIGHT
          marginTop: -1
        })
        const a = timeActions[totalTime] = timeActions[totalTime] || []
        a.push(t[1])
      }
    }

    this.timeActions = timeActions
    this.timeline = result
    this.start()
  },
  beforeDestroy () {
    if (this.timeId !== 0) {
      clearInterval(this.timeId)
    }
  },
  methods: {
    start (delay = 0) {
      if (this.timeId !== 0) {
        return
      }
      const innerStart = () => {
        const startedTime = new Date().getTime()
        const updater = () => {
          const nowTime = (new Date().getTime() - startedTime) / 1000
          const previousSeconds = parseInt(this.elapsedSeconds)
          const nowSeconds = parseInt(nowTime)
          this.elapsedSeconds = nowTime

          if (previousSeconds !== nowSeconds) {
            const actions = this.timeActions[nowSeconds + ADVANCE_TIME]
            if (actions) {
              var ssu = new SpeechSynthesisUtterance()
              ssu.text = actions[0]
              ssu.lang = 'ja-JP'
              speechSynthesis.speak(ssu)
            }
          }
        }
        updater()
        this.timeId = setInterval(updater, 1 / MAX_FPS * 1000)
      }
      if (delay > 0) {
        setTimeout(innerStart, delay * 1000)
      } else {
        innerStart()
      }
    }
  }
}
</script>
<style scoped>
.timeline-box {
  position: relative;
}
.action {
  position: absolute;
  width: 100%;
  margin-top: -1px;
  border-top: 1px solid;
  text-align: left;
  font: 14px black;
}
</style>
