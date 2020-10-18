<template>
  <span class="float-right" @click="onclick">
    <img src="/static/img/star_yl.png" width="16" height="16" v-if="is_bookmarked">
    <img src="/static/img/star_bk.png" width="16" height="16" v-else>
  </span>
</template>

<script>
export default {
  props: {
    id: {type: Number, required: true},
    is_bookmarked: {type: Boolean, required: false, default: false}
  },
  methods: {
    onclick () {
      console.log('bookmark clicked')
    }
  }
}
</script>