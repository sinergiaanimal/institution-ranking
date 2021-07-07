<template>
  <table class="ranking-browser-table table">
    <thead>
      <tr>
        <th scope="col">{{ cfg.instColName }}</th>
        <th scope="col">{# score #}</th>
        <th scope="col">Country</th>
        <th scope="col">Category 1</th>
        <th scope="col">Category 2</th>
        <th scope="col">Category 3</th>
        <th scope="col">Category 4</th>
        <th scope="col">Compare</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Sth</td>
        <td>Sth</td>
        <td>Sth</td>
        <td>Sth</td>
        <td>Sth</td>
        <td>Sth</td>
        <td>Sth</td>
        <td>Sth</td>
      </tr>
      <tr>
        <td>Sth</td>
        <td>Sth</td>
        <td>Sth</td>
        <td>Sth</td>
        <td>Sth</td>
        <td>Sth</td>
        <td>Sth</td>
        <td>Sth</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
module.exports = {
  props: {
    'cfg': {
      type: Object,
      required: true
    }
  },
  data () {
    return {
    };
  }
};
</script>
