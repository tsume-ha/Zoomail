<template>
  <ul>
    <li @click="clicked(page - 1)" :class="{ disabled: page === 1 }">
      <Icon icon="angle-left" />
    </li>
    <li @click="clicked(1)" v-if="page > 1">1</li>
    <li class="circle" v-if="page - 1 - 1 > 1"></li>
    <li @click="clicked(page - 1)" v-if="page - 1 > 1">
      {{ page - 1 }}
    </li>
    <li @click="clicked(page)" class="active">
      {{ page }}
    </li>
    <li @click="clicked(page + 1)" v-if="page + 1 < pages">
      {{ page + 1 }}
    </li>
    <li class="circle" v-if="pages - (page + 1) > 1"></li>
    <li @click="clicked(pages)" v-if="page < pages">
      {{ pages }}
    </li>
    <li @click="clicked(page + 1)" :class="{ disabled: page === pages }">
      <Icon icon="angle-right" />
    </li>
  </ul>
</template>

<script>
export default {
  props: {
    pages: { required: true, type: Number },
    page: { required: true, type: Number },
  },
  // setup(_props, context) {
  //   const clicked = page => {
  //     context.emit("pageTo", page);
  //   };
  //   return {
  //     clicked
  //   };
  // },
  methods: {
    clicked(pageTo) {
      this.$emit("pageTo", pageTo);
    },
  },
};
</script>

<style lang="scss" scoped>
ul {
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
  margin: 3rem 0 1rem;
  padding: 0;
  // background-color: $bg-dark;
  border-radius: 1rem;
  li {
    list-style: none;
    display: inline-block;
    box-sizing: border-box;
    text-align: center;
    margin: 0.5rem;
    padding: 0.65rem 0.4rem;
    min-width: 2.5rem;
    min-height: 2.5rem;
    line-height: 100%;
    font-size: 1rem;
    border-radius: 50%;
    background-color: $bg-light-lighten3;
    cursor: pointer;

    &.circle {
      min-width: 0.4rem;
      min-height: 0.4rem;
      padding: 0.1rem;
      cursor: default;
    }
    &.disabled {
      color: $text-dark;
    }
    &.active {
      background-color: $bg-light;
    }
  }
}
</style>