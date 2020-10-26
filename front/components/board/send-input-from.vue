<template>
  <div class="my-2">
    <div class="v-select-label">
     From: 
    </div>
    <select name="year_choice" v-model="selectedYear" class="form-control" id="year_choice">
      <option v-for="year in years" :value="year" :key="year">
        {{year}}
      </option>
    </select>
    <select name="member_choice" v-model="selectedMember" class="form-control" id="member_choice">
      <option v-for="member in memberChoices" :value="member.id" :key="member.id">
        {{member.name}}
      </option>
    </select>
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
  }),
  computed: {
    memberChoices () {
      return this.members[String(this.selectedYear)];
    }
  }
}
</script>

<style scoped>
.v-select-label{
  display: inline-block;
  width: 3rem;
}
#year_choice{
  display: inline-block;
  width: 5rem;
  padding: 6px;
}
#member_choice{
  display: inline-block;
  width: calc(100% - 9rem);
  min-width: 8rem;
  max-width: 18rem;
}
</style>