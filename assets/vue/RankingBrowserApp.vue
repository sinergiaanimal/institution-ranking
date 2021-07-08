<template>
  <table class="ranking-browser-table table">
    <thead>
      <tr>
        <th scope="col">{{ cfg.instColName }}</th>
        <th scope="col">Score</th>
        <th scope="col">Country</th>
        
        <th scope="col"
            v-for="category in policyCategories"
            :key="category.id">
          {{ category.name }}
        </th>
        
        <th scope="col">Compare</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="institution in institutions"
          :key="institution.id">
        <td>{{ institution.name }}</td>
        <td>{{ institution.scores.total }}</td>
        <td>{{ institution.country }}</td>

        <td scope="col"
            v-for="category in policyCategories"
            :key="category.id">
            {{ institution.scores[category.slug] }}
        </td>

        <th scope="col"></th>
      </tr>
    </tbody>
  </table>
</template>

<script>
import axios from 'axios';

const apiUrls = {
  institutions: '/api/institutions/',
  policyCategories: '/api/policy-categories/'
};

export default {
  props: {
    'cfg': {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      policyCategories: null,
      institutions: null
    }
  },
  async mounted () {
    await axios
      .get(apiUrls.policyCategories)
      .then(response => (this.policyCategories = response.data))
    await axios
      .get(apiUrls.institutions)
      .then(response => (this.institutions = response.data))
    
  }
};
</script>
