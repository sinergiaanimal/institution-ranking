<template>
  <div>
    <div id="comparer-popup"
         class="modal fade popup"
         tabindex="-1"
         role="dialog">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title popup__title">
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
            <table class="table comparison">
              <tr>
                <td scope="col" class="invisible category-col"></td>
                <th
                  scope="col"
                  v-for="(institution, index) in institutions"
                  :class="{
                    'corner-tl': index === 0,
                    'corner-tr': index === institutions.length - 1
                  }"
                  :key="institution.id"
                >
                  {{ institution.name }}
                </th>
              </tr>

              <tr v-for="(category, index) in categories"
                 :key="category.id">
                <th scope="col"
                    :class="{
                      'corner-tl': index === 0,
                      'corner-bl': index === categories.length - 1
                    }">
                  {{ category.name }}
                  </th>
                <td
                  v-for="institution in institutions"
                  :key="institution.id"
                  scope="col"
                >
                  {{ institution.scores[category.slug] }}
                </td>
              </tr>

              <tr>
                <th scope="col" class="bg-transparent">Total</th>
                <td
                  v-for="(institution, index) in institutions"
                  scope="col"
                  :key="institution.id"
                  :class="{
                    'corner-bl': index === 0,
                    'corner-br': index === institutions.length - 1
                  }"
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
