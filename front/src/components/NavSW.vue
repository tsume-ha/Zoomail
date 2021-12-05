<template>
  <button id="nav-sw" @click="onClicked">
    <span :class="[props.status]"></span>
  </button>
</template>

<script>
export default {
  props: {
    status: {
      required: true,
      validator: value => ["toMenu", "toClose", "toReturn"].indexOf(value) !== -1
    }
  },
  setup(props, context) {
    const onClicked = () => {
      context.emit("navSWClicked");
    };
    return {
      props,
      onClicked
    };
  },
};
</script>

<style lang="scss" scoped>
#nav-sw {
  position: relative;
  display: inline-block;
  height: 30px;
  width: 35px;
  background: transparent;
  border: 1px solid $text-white;
  border-radius: 8px;

  span,
  span::before,
  span::after {
    position:absolute;
    content:'';
    height:1px;
    width:20px;
    background: $text-white;
    display:block;
    transition: .5s;
  }
  span.toMenu{
    top:14px;
    left:7px;
  }
  span.toMenu::before{
    top:-6px;
    left:0;
  }
  span.toMenu::after{
    top:6px;
    left:0;
  }
  span.toClose{
    transform: rotate(-45deg);
  }
  span.toClose::before,
  span.toClose::after{
    top: 0px;
    left: 0px;
    transform: rotate(90deg);
  }

}

</style>