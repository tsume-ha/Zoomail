<template>
  <select v-model="value" @change="eventUp" class="form-control col-3 d-inline">
    <option
      v-for="i in 18"
      :key="i+8"
      :value="i+8"
      :disabled="!(minSafed <= i+8 && i+8 <= maxSafed)"
    >
      {{ i+8 }}:00
    </option>
  </select>
</template>

<script>
export default {
  props: {
    name: {type: String, required: true},
    min: {type: Number, required: false},//ここでdefault定義できない。nullの時効かない。
    max: {type: Number, required: false},
  },
  data: function(){
    return {
      value: null,
    };
  },
  methods: {
    eventUp: function(){
      this.$emit('onchange', {name: this.name, value: this.value});
    },
  },
  computed: {
    minSafed: function(){
      return this.min || 9;//nullの時propsでのdefaultを通り抜けるためここでdefault定義。
    },
    maxSafed: function(){
      return this.max || 26;
    }
  }
}
</script>