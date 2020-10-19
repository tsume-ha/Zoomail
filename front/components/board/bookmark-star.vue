<template>
  <span class="float-right" @click="onclick">
    <img src="/static/img/star_yl.png" width="16" height="16" v-if="bookmarked">
    <img src="/static/img/star_bk.png" width="16" height="16" v-else>
  </span>
</template>

<script>
export default {
  props: {
    id: {type: Number, required: true},
    is_bookmarked: {type: Boolean, required: false, default: false}
  },
  data: () => {
    return {
      bookmarked: false
    }
  },
  created () {
    this.bookmarked = this.is_bookmarked;
  },
  methods: {
    onclick () {
      this.axios.post('/read/api/bookmark/' + String(this.id) +'/', {
        'data': 'data'
      }).then(res => {
        this.bookmarked = (res.data['updated-to'] === 'true');
        this.$store.commit('read/updateBookmarked', {
          'id': this.id,
          'bool': (res.data['updated-to'] === 'true')
        })
      })
    }
  }
}
</script>