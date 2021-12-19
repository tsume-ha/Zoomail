<template>
  <div class="preview-content-wrapper" @click="openFile">
    <div v-if="(
        file.type === 'image/jpeg' ||
        file.type === 'image/png' ||
        file.type === 'image/bmp' ||
        file.type === 'image/gif' ||
        file.type === 'image/svg+xml'
      )" class="icon-wrapper">
      <img :src="imageURL" alt="image-preview" width="400" height="300" />
    </div>
    <div v-else-if="file.type === 'application/pdf'" class="icon-wrapper">
      <Icon icon="file-pdf" />
    </div>
    <div v-else-if="file.type.startsWith('audio/')" class="icon-wrapper">
      <Icon icon="file-audio" />
    </div>
    <div v-else-if="file.type.startsWith('video/')" class="icon-wrapper">
      <Icon icon="file-video" />
    </div>
    <div v-else-if="file.type === 'application/msword' || file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'" class="icon-wrapper">
      <Icon icon="file-word" />
    </div>
    <div v-else-if="file.type === 'application/vnd.ms-powerpoint' || file.type === 'vnd.openxmlformats-officedocument.presentationml.presentation'" class="icon-wrapper">
      <Icon icon="file-powerpoint" />
    </div>
    <div v-else-if="file.type === 'application/vnd.ms-excel' || file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'" class="icon-wrapper">
      <Icon icon="file-excel" />
    </div>
    
    <div v-else class="icon-wrapper">
      <Icon icon="file-alt" />
    </div>
    
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
      if (isImage.value) {
        reader.onload = e => {
          imageURL.value = e.target.result;
        };
      }
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

<style lang="scss" scoped>
.preview-content-wrapper{
  display: inline-block;
  position: relative;
  align-self: center;
  width: 9rem;
  height: 8rem;
  border: 1px solid #aaa;
  border-radius: 0.3rem;
  margin: 0.5rem;
  padding: .5rem;
  z-index: 1;
  cursor: pointer;
  background-color: $bg-white;

  .icon-wrapper {
    display: block;
    position: relative;
    width: 100%;
    height: 100%;
    margin: 0 auto;
    text-align: center;

    img, svg{
      display: block;
      margin: 0 auto;
    }
    img {
      width: 100%;
      height: auto;
      object-fit: contain;
    }
    svg {
      width: 4rem;
      height: auto;
    }
  }

  .preview-file-name{
    position: absolute;
    bottom: 0.5rem;
    font-size: 0.6rem;
  }
}
</style>