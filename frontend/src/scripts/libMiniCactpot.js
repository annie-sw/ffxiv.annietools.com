// ナンバーボードの値リスト
const ALL_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]

// スコアリスト
const SCORES = {
  6: 10000,
  7: 36,
  8: 720,
  9: 360,
  10: 80,
  11: 252,
  12: 108,
  13: 72,
  14: 54,
  15: 180,
  16: 72,
  17: 180,
  18: 119,
  19: 36,
  20: 306,
  21: 1080,
  22: 144,
  23: 1800,
  24: 3600
}

// 列とインデックスリストの対応表
const LINES = {
  // 縦
  2: [0, 3, 6],
  3: [1, 4, 7],
  4: [2, 5, 8],
  // 横
  6: [0, 1, 2],
  7: [3, 4, 5],
  8: [6, 7, 8],
  // 斜め
  1: [0, 4, 8],
  5: [2, 4, 6]
}

const sum = (arr) => arr.reduce((prev, current, i, arr) => { return prev + current }, 0)
const avg = (arr) => sum(arr) * 1.0 / arr.length

export default {
  consts: {
    scores: SCORES,
    lines: LINES
  },

  // 0で埋めた9要素の配列を返す
  newBoard () {
    let board = Array(ALL_VALUES.length)
    for (let i = 0; i < board.length; ++i) {
      board[i] = 0
    }
    return board
  },

  // values の組み合わせを返す
  getValueCombinations (values, level) {
    if (level === 1) {
      let ret = []
      for (let v of values) {
        ret.push([v])
      }
      return ret
    }

    let ret = []
    let poped = []
    for (let x of values) {
      poped.push(x)
      for (let y of this.getValueCombinations(values.filter((x) => poped.indexOf(x) < 0), level - 1)) {
        ret.push([x].concat(y))
      }
    }
    return ret
  },

  // 値が0のインデックスリストを返す
  getFreeIndexes (board) {
    let ret = []
    for (let i = 0; i < ALL_VALUES.length; ++i) {
      if (board[i] === 0) {
        ret.push(i)
      }
    }
    return ret
  },

  // ラインの値リストを返す
  getLineValues (board, lineId) {
    let values = []
    for (let i of LINES[lineId]) {
      if (board[i] !== 0) {
        values.push(board[i])
      }
    }
    return values
  },

  // board と fixedValues に存在しない ALL_VALUES の値の組み合わせを返す
  getPossibleValues (board, fixedValues) {
    let level = 3 - fixedValues.length
    if (level === 0) {
      return [fixedValues]
    }

    let candidateValues = []
    for (let candidateValue of ALL_VALUES) {
      if (board.indexOf(candidateValue) < 0 && fixedValues.indexOf(candidateValue) < 0) {
        candidateValues.push(candidateValue)
      }
    }

    let ret = []
    for (let expectedValues of this.getValueCombinations(candidateValues, 3 - fixedValues.length)) {
      ret.push(expectedValues.concat(fixedValues))
    }
    return ret
  },

  // lineId で期待されるスコアのリストを返す
  getExpectedScores (board, lineId) {
    let ret = []
    let fixedValues = this.getLineValues(board, lineId)
    for (let expectedValues of this.getPossibleValues(board, fixedValues)) {
      ret.push(SCORES[sum(expectedValues)])
    }
    return ret
  },

  // インデックス毎の期待値を取得
  getScoresPerIndex (board) {
    let freeIndexes = this.getFreeIndexes(board)

    let ret = []
    for (let index of freeIndexes) {
      // インデックスが含まれる列の期待値を取得
      let expectedScoresPerLine = []
      for (let i in LINES) {
        if (LINES[i].indexOf(index) >= 0) {
          let values = this.getExpectedScores(board, i)
          expectedScoresPerLine.push(avg(values))
        }
      }
      ret.push({
        index: index,
        score: sum(expectedScoresPerLine)
      })
    }
    return ret
  },

  // 列毎の期待値を取得
  getScoresPerLine (board) {
    let ret = []
    for (let lineId in LINES) {
      let values = this.getExpectedScores(board, lineId).sort((a, b) => b - a)
      ret.push({
        id: lineId,
        score: avg(values),
        values: values
      })
    }
    return ret
  }
}
