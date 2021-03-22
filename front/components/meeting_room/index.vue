<template>
  <div>
    <h3>例会教室</h3>
    <div>
      <router-link
      v-if="is_staff"
        to="./register/"
        class="btn btn-warning mb-3">修正・登録</router-link>
      <p v-if="rooms.length === 0">
        Now Loading...
      </p>
      <table v-else class="table">
        <tr
          v-for="data in rooms" :key="data.date"
        >
          <td>
            <span :class="data.date | dayColor">
              {{ data.date | md }}
            </span>
          </td>
          <td>
            <span :class="data.room | roomColor">
              {{ data.room | room }}
            </span>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import moment from 'moment/moment'
moment.locale('ja')
export default {
  data: function() {
    return {
      rooms: [],
      is_staff: false,
    }
  },
  metaInfo: {
    title: '例会教室'
  },
  created: function() {
    this.axios
      .get('/api/meeting_room/get31day/')
      .then(res => {
        this.rooms = res.data.rooms
      })
    this.axios
      .get('/api/meeting_room/')
      .then(res => {
        this.is_staff = res.data.meeting_room_permission
      })
  },
  filters: {
    md: function(date) {
      return moment(date).format('MM/DD (dd)')
    },
    dayColor(date) {
      let day = moment(date).format('d')
      switch (day) {
        case '0':
          return 'text-danger'
          break
        case '6':
          return 'text-primary'
          break
        default:
          return ''
          break
      }
    },
    room(room) {
      switch (room) {
        case null:
          return '例会教室は未登録'
          break
        default:
          return room
          break
      }
    },
    roomColor(room) {
      switch (room) {
        case '終日使用不可':
        case '使用不可':
          return 'text-danger'
          break
        case null:
          return 'text-muted'
          break
        case '(20時まで音出し不可)':
          return 'text-success'
          break
        default:
          return ''
          break
      }
    }
  }
}
</script>