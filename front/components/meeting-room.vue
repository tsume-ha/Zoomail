<template>
  <div class="p-2" v-if="today">
    <h4>例会教室</h4>
    <span v-if="yesterday">
      今日({{ yesterday | moment("MM/DD") }})の AM 5:00までの例会教室は <br />
      <b>{{ yesterdayRoom }}</b
      >,<br /><br />
      今日({{ today | moment("MM/DD") }})の例会教室は <br /><b>{{ todayRoom }}</b> です.
    </span>
    <span v-else>
      今日({{ today | md }})の例会教室は <br />
      <b>{{ todayRoom }}</b> です.
    </span>
  </div>
</template>
<script>
import moment from "moment"
export default {
  data: function() {
    return {
      todayRoom: "データなし",
      today: moment().format('YYYY-MM-DD'),
      yesterdayRoom: "",
      yesterday: "",
    };
  },
  created: function() {
    this.axios
      .get("https://meetingroomcontroller.appspot.com/room/today")
      .then((res) => {
        this.todayRoom = res.data.room;
        this.today = res.data.date;
        this.yesterday = res.data["date-before"];
        this.yesterdayRoom = res.data["room-before"];
      });
  },
  filters: {
    md: function(date) {
      return moment(date).format("MM/DD");
    },
  },
};
</script>
<style scoped>
div {
  border: 1px solid #463100;
  border-radius: 4px;
  background-color: #ffffcc;
}
div h4 {
  font-size: 1.2rem;
}
div p span {
  display: inline-block;
}
div p span:nth-child(1),
div p span:nth-child(3) {
  font-size: 0.8rem;
}
div p span:nth-child(2) {
  font-size: 1rem;
  font-weight: 600;
}
</style>
