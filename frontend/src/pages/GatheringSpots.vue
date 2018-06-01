<template>
  <div>
    <div v-for="item in items" v-bind:key="'item:' + item.itemId()">
      <span>{{ $store.state.General.text.itemNames(item.itemId()) }}</span> =>
      <span v-for="(spot, spotIndex) in getSpots(item)" v-bind:key="'spot:' + spotIndex">
        {{ $store.state.General.text.placeNames(spot.spotId()) }}
      </span>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      items: []
    }
  },

  methods: {
    getSpots (item) {
      const spots = Array(item.spotsLength())
      for (let i = item.spotsLength() - 1; i >= 0; --i) {
        spots[i] = item.spots(i)
      }
      return spots
    }
  },

  mounted () {
    const data = this.$store.state.General.data
    console.log(data, data.gatheringItemsLength())
    this.items = Array(data.gatheringItemsLength())
    for (let i = data.gatheringItemsLength() - 1; i >= 0; --i) {
      const item = data.gatheringItems(i)
      this.items[i] = item
    }
  }
}
</script>

<style>
</style>
