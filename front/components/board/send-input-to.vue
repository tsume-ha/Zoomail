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
  data: () => ({
      isTouched: false,
  }),
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
    years () {
      return this.$store.state.send.to_groups;
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