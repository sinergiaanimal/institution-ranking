<template>
  <div>
    <div id="comparer-popup" class="modal fade" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title">
              {{ popupTitle }}
            </h1>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <table class="table">
              <tr>
                <th scope="col"></th>
                <th
                  scope="col"
                  v-for="institution in institutions"
                  :key="institution.id"
                >
                  {{ institution.name }}
                </th>
              </tr>

              <tr v-for="category in categories" :key="category.id">
                <th scope="col">{{ category.name }}</th>
                <td
                  v-for="institution in institutions"
                  :key="institution.id"
                  scope="col"
                >
                  {{ institution.scores[category.slug] }}
                </td>
              </tr>
              <tr>
                <th scope="col">TOTAL</th>
                <td
                  v-for="institution in institutions"
                  :key="institution.id"
                  scope="col"
                >
                  {{ institution.scores.total }}
                </td>
              </tr>
            </table>
          </div>
        </div>
      </div>
    </div>
    <div
      class="toast-panel toast-panel--br-corner"
      v-show="institutions.length > 0"
    >
      <p>{{ popupInfo }}</p>
      <button
        type="button"
        class="button button--primary button--with-counter ml-3"
        @click="showPopup()"
      >
        <span class="button__text">Compare</span>
        <span class="button__counter">{{
          institutions.length
        }}</span>
      </button>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';

export default {
  props: {
    popupTitle: String,
    popupInfo: String,
    institutions: Array,
    categories: Array,
  },

  data () {
    return {};
  },

  methods: {
    showPopup () {
      $('#comparer-popup').modal('show');
      console.log(this.institutions);
    },
  },
};
</script>
