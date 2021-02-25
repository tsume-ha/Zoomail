<template>
  <div>
  <div class="my-2">
    <div class="v-select-label">
     From: 
    </div>
    <select name="year_choice" v-model="selectedYear" class="form-control" id="year_choice">
      <option v-for="year in years" :value="year" :key="year">
        {{year}}
      </option>
    </select>
    <select name="member_choice" v-model="selectedMember" class="form-control" id="member_choice">
      <option v-for="member in memberChoices" :value="member.id" :key="member.id">
        {{member.name}}
      </option>
    </select>
  </div>
  <validation-error-messages
    v-if="is_valid.length > 0 && isValidationDisplay"
    :messages="is_valid" />
  </div>
</template>

<script>
import validationErrorMessages from './send-validation-error.vue';
export default {
  components: {
    validationErrorMessages
  },
  computed: {
    selectedMember: {
      get () {
        return this.$store.state.send.writer_id;
      },
      set (value) {
        this.$store.commit('send/fromInput', value);
      }
    },
    selectedYear: {
      get () {
        return this.$store.state.send.writer_year;
      },
      set (value) {
        this.$store.commit('send/setWriterYear', value);
      }
    },
    years () {
      return this.$store.state.send.writer_years;
    },
    members () {
      return this.$store.state.send.writer_choices;
    },
    memberChoices () {
      const tmp = this.members.find(obj => obj.year === this.selectedYear);
      if (tmp) {
        return tmp.list;
      }
      return [];
    },
    is_valid () {
      return this.$store.getters['send/validateWriter'];
    },
    isValidationDisplay () {
      return this.$store.state.send.validate_clicked;
    }
  }
}
</script>

<style scoped>
.v-select-label{
  display: inline-block;
  width: 3rem;
}
#year_choice{
  display: inline-block;
  width: 5rem;
  padding: 6px;
}
#member_choice{
  display: inline-block;
  width: calc(100% - 9rem);
  min-width: 8rem;
  max-width: 18rem;
}
</style>