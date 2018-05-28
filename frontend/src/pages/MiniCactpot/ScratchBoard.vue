<template>
  <div class="panel panel-default">
    <table id="scratch-board" class="table table-bordered">
      <tbody>
        <tr>
          <th v-bind:class="[{ expected: isExpectedLine(1) }, 'col-xs-1 col-sm-1']">1</th>
          <th v-bind:class="[{ expected: isExpectedLine(2) }, 'col-xs-3 col-sm-3']">2</th>
          <th v-bind:class="[{ expected: isExpectedLine(3) }, 'col-xs-3 col-sm-3']">3</th>
          <th v-bind:class="[{ expected: isExpectedLine(4) }, 'col-xs-3 col-sm-3']">4</th>
          <th v-bind:class="[{ expected: isExpectedLine(5) }, 'col-xs-1 col-sm-1']">5</th>
        </tr>
      <tr>
        <th v-bind:class="{ expected: isExpectedLine(6) }">6</th>
        <td v-for="i in range(0, 2)"
            v-bind:class="{duplicated: isDuplicated(i), expected: isExpected(i)}"
            v-on:click="selectIndex(i)"
            v-bind:key="'scratch-panel:' + i">{{ dispNumber(i) }}</td>
        <td rowspan="3" class="etc">
            <button class="btn btn-default" v-on:click="reset">Reset</button>
        </td>
      </tr>
      <tr>
        <th v-bind:class="{ expected: isExpectedLine(7) }">7</th>
        <td v-for="i in range(3, 5)"
            v-bind:class="{duplicated: isDuplicated(i), expected: isExpected(i)}"
            v-on:click="selectIndex(i)"
            v-bind:key="'scratch-panel:' + i">{{ dispNumber(i) }}</td>
      </tr>
      <tr>
        <th v-bind:class="{ expected: isExpectedLine(8) }">8</th>
        <td v-for="i in range(6, 8)"
            v-bind:class="{duplicated: isDuplicated(i), expected: isExpected(i)}"
            v-on:click="selectIndex(i)"
            v-bind:key="'scratch-panel:' + i">{{ dispNumber(i) }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'scratch-board',
  data () {
    return {
      duplicatedIndexes: []
    }
  },
  props: ['board', 'expectedIndexes', 'selectedLine'],
  computed: {
    highScoreIndexes () {
      if (this.expectedIndexes === null) {
        return null
      }

      let score = Math.max(...this.expectedIndexes.map(x => x.score))
      let indexes = []
      for (let x of this.expectedIndexes) {
        if (x.score === score) {
          indexes.push(x.index)
        }
      }
      return indexes
    }
  },

  methods: {
    range (start, end) {
      let ret = Array(end - start + 1)
      for (let i = 0; i < ret.length; ++i) {
        ret[i] = start + i
      }
      return ret
    },

    // 表示する値を返す
    dispNumber (index) {
      const num = this.board[index]
      return num || ''
      // return num ? num : ''
    },

    // 初期化
    reset () {
      this.duplicatedIndexes = []
      this.$emit('reset')
    },

    // 重複チェック
    validate () {
      let indexes = []
      let values = this.board.filter((x, i, self) => {
        return x > 0 && self.indexOf(x) === i && i !== self.lastIndexOf(x)
      })
      this.board.forEach((v, i) => {
        if (values.indexOf(v) >= 0) {
          indexes.push(i)
        }
      })

      this.duplicatedIndexes = indexes

      return indexes.length === 0
    },

    // クリックイベント
    selectIndex (index) {
      // 重複値がある場合、他の場所は入力出来ないよ
      if (this.duplicatedIndexes.length > 0 && this.duplicatedIndexes.indexOf(index) < 0) {
        return
      }
      this.$emit('selectIndex', index, this.validate) // 親へイベント通知
    },

    // 重複 classObject
    isDuplicated (index) {
      return this.duplicatedIndexes && this.duplicatedIndexes.indexOf(index) >= 0
    },

    // 期待するインデックスの classObject
    isExpected (index) {
      if (this.highScoreIndexes) {
        return this.highScoreIndexes.indexOf(index) >= 0
      }
      if (this.selectedLine) {
        return this.selectedLine['indexes'].indexOf(index) >= 0
      }
      return false
    },

    // 選択された列の classObject
    isExpectedLine (id) {
      return this.selectedLine && this.selectedLine['id'] === id
    }
  }
}
</script>

<style>
/* #scratch-board .selected { */
    /* color: #666666; */
    /* background-color: #ccffcc; */
/* } */
#scratch-board .duplicated {
    background-color: #ffcccc;
}
#scratch-board .expected {
    background-color: #ccffff;
}
#scratch-board th.expected {
    color: #666666;
}
/* #scratch-board .expected-2 { */
    /* background-color: #ccffcc; */
/* } */
#scratch-board th {
    text-align: center;
    vertical-align: middle;
    color: #ffffff;
    background-color: #666666;
    height: 60px;
}
#scratch-board td {
    text-align: center;
    vertical-align: middle;
}
#scratch-board td.etc {
    text-align: center;
    vertical-align: bottom;
}
#scratch-board {
    /* position: relative; */
}
</style>
