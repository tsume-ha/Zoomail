<template>
  <read-index :sendboxMode="true" />
</template>

<script>
// import nowloading from '../nowloading.vue';
import index from '../board/index';
export default {
  name: 'mypage-sendbox',
  components: {
    readIndex: index,
  },
  metaInfo: {
    title: '送信ボックス'
  },
  // created() {
  //   this.getMessage()
  // },
  // data: () => ({
  // }),
  // computed: {
  // },
  // methods: {
  //   getMessage () {
  //     this.axios.get('/api/board/json/', {params:{'sendbox': true}})
  //     .then(res => {
  //       console.log(res)
  //     })
  //   }
  // }
}
</script>