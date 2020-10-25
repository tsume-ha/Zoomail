<template>
  <div class="my-2">
    <div class="v-select-label">
     From: 
    </div>
    <div class="v-select-wraper-year">
      <v-select
        v-model="selectedYear"
        :options="years"
        :clearable="false"
      ></v-select>
    </div>
    <div class="v-select-wraper-member">
      <v-select
        v-model="selectedMember"
        :options="members[selectedYear]"
        label="name"
        :reduce="obj=>obj.id"
        :clearable="false"
      ></v-select>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    years: [2020, 2019, 2018, 2017],
    selectedYear: 2018,
    members: {
      '2018': [
        {id:1,name:'あああああ'},{id:2,name:'い'},{id:3,name:'う'}
      ]
    },
    selectedMember: null
  })
}
</script>

<style scoped>
.v-select-label{
  display: inline-block;
  width: 3rem;
}
.v-select-wraper-year{
  display: inline-block;
  min-width: 6rem;
  width: 40%;
}
.v-select-wraper-member{
  display: inline-block;
  width: calc(60% - 4rem);
  min-width: 8rem;
}
</style>