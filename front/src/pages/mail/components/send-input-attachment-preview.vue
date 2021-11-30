<template>
  <div class="preview-content-wrapper" @click="openFile">
    <img v-if="isImage" :src="imageURL" alt="iamge-preview">
    <img v-else-if="file.type=='application/pdf'" src="/static/img/board/pdf-icon.png" alt="pdf-icon">
    <img v-else src="/static/img/board/file-icon.png" alt="file-icon">
    <div class="preview-file-name">{{file.name}}</div>
  </div>
</template>

<script>
import { computed, ref, onMounted, onUnmounted } from "vue";
export default {
  props: {
    file: {required: true, type: File}
  },
  setup(props) {
    const imageURL = ref("");
    const objectURL = ref("");
    const file = computed(() => props.file);

    const isImage = computed(() => file.value.type.startsWith("image/"));

    const openFile = () => {
      if (objectURL.value) {
        window.open(objectURL.value, "filePreview");
      }
    };
    onMounted(() => {
      const reader = new FileReader();
      reader.onload = e => {
        imageURL.value = e.target.result;
      };
      reader.readAsDataURL(file.value);
      objectURL.value = URL.createObjectURL(file.value);
    });


    onUnmounted(() => {
      URL.revokeObjectURL(file.value);
    });
    return {
      openFile, isImage, imageURL
    };
  }
};
</script>

<style scoped>
.preview-content-wrapper{
  border: 1px solid #aaa;
  border-radius: 0.3rem;
  margin: 0.5rem;
  padding: 0.5rem;
  z-index: 1;
  cursor: pointer;
}
img{
  width: 8rem;
  height: 6rem;
  object-fit: contain;
}
.preview-file-name{
  font-size: 0.6rem;
}
</style>