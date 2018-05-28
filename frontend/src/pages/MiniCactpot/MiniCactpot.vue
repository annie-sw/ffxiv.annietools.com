<template>
  <div>
    <ScratchBoard v-bind:board="board"
                  v-bind:expectedIndexes="expectedIndexes"
                  v-bind:selectedLine="selectedLine"
                  v-on:reset="reset"
                  v-on:selectIndex="selectIndex" />

    <ExpectedTable v-if="expectedLines"
                   v-bind:expectedLines="expectedLines"
                   v-on:selectLine="selectLine" />

    <NumberPanels v-if="showNumberPanels"
                  v-bind:board="board"
                  v-bind:selectNumber="selectNumber" />
  </div>
</template>

<script>
import logic from '@/scripts/libMiniCactpot'
import ScratchBoard from './ScratchBoard'
import ExpectedTable from './ExpectedTable'
import NumberPanels from './NumberPanels'

export default {
  name: 'app',
  components: {
    ScratchBoard,
    ExpectedTable,
    NumberPanels
  },
  data () {
    return {
      showNumberPanels: false,
      selectNumber: null,
      board: [],
      expectedIndexes: null,
      expectedLines: null,
      selectedLine: null
    }
  },
  methods: {

    // 状態初期化
    reset () {
      this.board = logic.newBoard()
      this.expectedIndexes = null
      this.expectedLines = null
      this.selectedLine = null
    },

    // ScratchBoard のクリックイベント
    selectIndex (index, validate) {
      let getPhase = () => this.board.filter(x => x > 0).length

      // ４マス以上入力してたら、未入力のマスは入力出来ないよ
      if (getPhase() >= 4 && this.board[index] === 0) {
        return
      }

      this.showNumberPanels = true
      this.selectNumber = (number) => { // NumberPanels のクリックイベント
        this.selectNumber = null
        this.showNumberPanels = false

        if (number >= 0) {
          this.expectedIndexes = null
          this.expectedLines = null
          this.selectedLine = null

          this.board.splice(index, 1, number)
          if (validate()) {
            this.calcExpection(getPhase())
          }
        }
      }
    },

    // ExpectedTable のクリックイベント
    selectLine (lineId) {
      this.selectedLine = {
        id: lineId,
        indexes: logic.consts.lines[lineId]
      }
    },

    // 候補の選出
    calcExpection (phase) {
      if (phase < 4) {
        // パネル単位でスコアリング
        this.expectedIndexes = logic.getScoresPerIndex(this.board)
      } else {
        // 列単位でスコアリング
        this.expectedLines = logic.getScoresPerLine(this.board)
      }
    }
  },

  // 初期化
  mounted () {
    this.reset()
  }
}
</script>

<style>
#app {
  margin: 0 auto;
  max-width: 800px;
}
</style>
