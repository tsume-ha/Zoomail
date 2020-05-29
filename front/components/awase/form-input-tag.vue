<template>
  <input :type="type" :name="name" :id="'id_'+name">
</template>

<script>
export default {
  props: ['type', 'name', 'init'],
  data: function(){
    return {
      value: this.init,
    }
  },
}
</script>