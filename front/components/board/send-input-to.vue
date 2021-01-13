<template>
  <div>
    <div class="my-2">
      <div class="v-select-label">
      To: 
      </div>
      <div class="v-select-wraper">
        <v-select
          v-model="selected"
          :options="years"
          label="label"
          :reduce="obj => obj.year"
          multiple
        ></v-select>
      </div>
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
  data: () => {
    return {
      years: [
        {'year': 0, 'label': '全回メーリス'},
        {'year': 2020, 'label': '2020 26期'},
        {'year': 2019, 'label': '2019 25期 会長：'},
        {'year': 2018, 'label': '2018 24期 会長：'},
      ],
      isTouched: false,
    }
  },
  computed: {
    selected: {
      get() {
        return this.$store.state.send.to;
      },
      set(value) {
        this.isTouched = true;
        this.$store.commit('send/toInput', value);
      }
    },
    is_valid () {
      return this.$store.getters['send/validateTo'];
    },
    isValidationDisplay () {
      return this.$store.state.send.validate_clicked || this.isTouched;
    }
  }
}
</script>

<style scoped>
.v-select-label{
  display: inline-block;
  width: 3rem;
}
.v-select-wraper{
  display: inline-block;
  width: calc(100% - 4rem);
}
</style>