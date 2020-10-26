<template>
  <section>
    <h3>メーリス送信</h3>
    <form class="my-3">
      <div
        class="col-sm-12 col-md-10 col-lg-8 p-0"><input-title /></div>
      <div
        class="col-sm-12 col-md-10 col-lg-8 p-0"><input-from /></div>
      <div
        class="col-sm-12 col-md-10 col-lg-8 p-0"><input-to /></div>
      <div
        class="col-sm-12 col-md-10 col-lg-8 p-0"><input-content /></div>
      <div
        class="col-sm-12 col-md-10 col-lg-8 p-0"><input-attachment /></div>
      <!-- <div
        class="col-sm-12 col-md-10 col-lg-8 p-0"><input-send-at /></div> -->
    </form>
  </section>
</template>

<script>
import inputTitle from './send-input-title.vue';
import inputFrom from './send-input-from.vue';
import inputTo from './send-input-to.vue';
import inputContent from './send-input-content.vue';
import inputAttachment from './send-input-attachment.vue';
import inputSendAt from './send-input-sendat.vue';
export default {
  components: {
    inputTitle,
    inputFrom,
    inputTo,
    inputContent,
    inputAttachment,
    inputSendAt
  },

}
</script>