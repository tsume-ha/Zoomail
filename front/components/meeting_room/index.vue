<template>
  <div>
    <h3>例会教室</h3>
    <div>
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
import moment from 'moment';
moment.locale('ja', {
  weekdays: ["日曜日", "月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日"],
  weekdaysShort: ["日", "月", "火", "水", "木", "金", "土"],
});
export default {
  data: function() {
    return {
      rooms: [],
      fields: [
        {
          key: 'date',
          thStyle: {
            display: 'none'
          }
        },
        {
          key: 'room',
          thStyle: {
            display: 'none'
          }
        }
      ]
    }
  },
  created: function() {
    this.axios
      .get('/api/meeting_room/get31day/')
      .then(res => {
        this.rooms = res.data.rooms
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