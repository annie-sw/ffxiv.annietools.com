import Vue from 'vue'
import Vuex from 'vuex'

import {flatbuffers} from '@/assets/flatbuffers'
import {Eorzea} from '@/assets/generated/db_generated'
// import {Eorzea} from '@/assets/generated/textdb_generated'

Vue.use(Vuex)

const General = {
  namespaced: true,
  state: {
    data: null,
    text: null
  },
  mutations: {
    setData (state, { data, text }) {
      state.data = Eorzea.DB.getRootAsDB(new flatbuffers.ByteBuffer(new Uint8Array(data)))
      state.text = Eorzea.TextDB.getRootAsTextDB(new flatbuffers.ByteBuffer(new Uint8Array(text)))
    }
  },
  getters: {
    getData (state) {
      return state.data
    }
  }
}

export default new Vuex.Store({
  modules: { General }
})
