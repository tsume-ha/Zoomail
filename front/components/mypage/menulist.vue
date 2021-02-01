<template>
  <section class="list-group list-group-flush col-sm-6 col-lg-4 mb-4">

    <!-- headerのlink pathが無いときは<h6> -->
    <router-link
        v-if="header.path"
        :to="header.path"
        class="list-group-item list-group-item-action border-left"
        :class="[colorClass]">
        {{header.text}}
    </router-link>
    <h6 v-else
        class="list-group-item list-group-item-action border-left disabled"
        :class="[colorClass]">
        {{header.text}}
    </h6>

    <!-- vueRouterがfalseに設定されているなら<a>タグに -->
    <template v-for="item in menu">

      <router-link
          v-if="item.vueRouter !== false"
          :key="item.text"
          :to="item.path"
          class="list-group-item list-group-item-action">
        {{item.text}}
      </router-link>

      <a
          v-else
          :key="item.text"
          :href="item.path"
          class="list-group-item list-group-item-action">
        {{item.text}}
      </a>

    </template>

 </section>

</template>

<script scoped>
export default {
  name: 'menulist',
  props: {
    borderColorClass: {required: false, type: String},
    // bootstrap で使われるClass名でborderの色を決める

    header: {required: true, type: Object},
    // menu の小見出しになる
    // header: {text: String, peth: String}

    menu: {required: false, default: [], type: Array}
    // 各menu のtext とリンク先情報
    // menu: [
    //   {text: String, path: String, vueRouter: Boolean}, ...
    // ]                              falseのみ定義可能, falseが明示されたときには<a>タグをレンダリングする
  },
  computed: {
    colorClass () {
      const preserved = ['primary','secondary','success','danger','warning','info','light','dark','white']
      if (preserved.includes(this.borderColorClass)) {
        return 'border-' + this.borderColorClass;
      }
      return '';
    }
  }
}
</script>

<style type="text/css">
section :first-child{
  font-size: 1.25rem;
  color: #212529 !important;
  border-top: none;
  border-left-width: 0.5rem!important;
  padding-left: 0.75rem;
}
section :last-child{
  border-bottom: 1px solid rgba(0,0,0,.125) !important;
}
</style>


