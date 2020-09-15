<template>
  <div>{{message.title}}</div>
</template>

<script>
export default {
  props: {
    message: {type: Object, required: true},
  },
}
</script>