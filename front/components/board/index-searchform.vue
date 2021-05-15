<template>
  <form class="content row pb-3 border-bottom" @submit="submit">
    <div class="col-12">
      <div class="d-inline-block">
        <input type="checkbox" name="is_kaisei" class="d-none" id="is_kaisei" v-model="is_kaisei" @change="toggleChanged">
        <label for="is_kaisei">回生メーリスのみ:</label>
      </div>
      <div class="d-inline-block">
        <input type="checkbox" name="is_zenkai" class="d-none" id="is_zenkai" v-model="is_zenkai" @change="toggleChanged">
        <label for="is_zenkai">全回メーリスのみ:</label>
      </div>
      <div class="d-inline-block">
        <input type="checkbox" name="is_bookmark" class="d-none" id="is_bookmark" v-model="is_bookmark" @change="toggleChanged">
        <label for="is_bookmark">ブックマークのみ:</label>
      </div>
      <div class="d-inline-block">
        <input type="checkbox" name="is_sender" class="d-none" id="is_sender" v-model="is_sender" @change="toggleChanged">
        <label for="is_sender">送信したメーリスのみ:</label>
      </div>
    </div>
    <div class="col-12 my-2" v-if="showButton">
      <input type="submit" value="絞り込み" class="submit btn btn-warning btn-sm ml-2">
    </div>
    <div class="col-12">
      <input type="text" name="text" placeholder="件名・本文で検索" class="form-control formtext" id="id_text" v-model="text">
      <input type="submit" value="検索" class="submit btn btn-info btn-sm ml-2">
    </div>
  </form>
</template>

<script>
export default {
  name: 'searchform',
  data: () => {
    return {
      is_kaisei: false,
      is_zenkai: false,
      is_bookmark: false,
      is_sender: false,
      text: '',
      showButton: false,
    }
  },
  methods: {
    toggleChanged () {
      this.showButton = true;
    },
    submit (e) {
      e.preventDefault();

      if (
           !this.is_kaisei
        && !this.is_kaisei
        && !this.is_bookmark
        && !this.is_sender
      ) {
        this.showButton = false;
      }

      const data = {
        is_kaisei: this.is_kaisei,
        is_zenkai: this.is_zenkai,
        is_bookmark: this.is_bookmark,
        is_sender: this.is_sender,
        text: this.text,
      };
      this.$emit('search', data)
    }
  }
}
</script>


<style scoped>

input.formtext{
  display: inline-block;
  width: calc(100% - 62px);
  max-width: 400px;
}


label{
    display: inline-block;
    position: relative;
    height: 1rem;
    padding: 0.5rem 3rem 1rem 0;
    margin: 0 0 0.5rem;
    font-size: 0.7rem;
    line-height: 0.7rem;
}
label:before{
  display: inline-block;
  content: "";
  position: absolute;
    right: 0.4rem;
    top: 0.3rem;
  width: 2.4rem;
  height: 1.2rem;
  margin: 0;
  padding: 0;
  border: 1px solid #999;
  border-radius: 1rem;
  transition: 0.2s;
}
label:after{
  display: block;
  content: "";
  position: absolute;
  top: 0.44rem;
  right: 1.7rem;
  width: 0.9rem;
  height: 0.9rem;
  border-radius: 0.75rem;
  background-color: #999;
  transition: 0.2s;
}
input:checked + label:before{
  border-color: #0ee08a;
}
input:checked + label:after{
  right: 0.62rem;
  background-color: #0ee08a;
}

</style>