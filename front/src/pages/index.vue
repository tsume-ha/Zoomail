<template>
  <div>
    <h1>index</h1>
    text{{counter}}
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from '../utils/axios'
// import axios from 'axios'
export default {
  setup(props) {
    const counter = ref(0)
    console.log(props)

    // const announcements = ref([])
    const getAnnouncementsAndContentLogs = axios({
        method: 'get',
        url: '/api/home/index/',
      }).then(response =>{
        console.log(response)
      })
    onMounted(getAnnouncementsAndContentLogs)
    return{
      counter,
    }
  }
}
</script>