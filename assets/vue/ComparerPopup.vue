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

          <div class="modal-body overflow-x-scroll">
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
                  <span class="value">
                    {{ institution.name }}
                  </span>
                </th>
              </tr>

              <tr v-for="(category, index) in categories"
                 :key="category.id">
                <th scope="col"
                    :class="{
                      'corner-tl': index === 0,
                      'corner-bl': index === categories.length - 1
                    }">
                  <span class="value">
                    {{ category.name }}
                  </span>
                </th>
                <td
                  v-for="(institution, i) in institutions"
                  scope="col"
                  :key="institution.id"
                >
                  <span 
                    :class="{
                      'value': true,
                      'value--positive': evaluated[i][category.slug].isPositive,
                      'value--neutral': evaluated[i][category.slug].isNeutral,
                      'value--negative': evaluated[i][category.slug].isNegative
                    }"
                  >
                    {{ institution.scores[category.slug] }}<!--
                    -->/{{ category.max_score }}
                  </span>
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
                  <span
                    :class="{
                      'value': true,
                      'value--summary-positive':
                        evaluated[index]['total'].isPositive,
                      'value--summary-neutral':
                        evaluated[index]['total'].isNeutral,
                      'value--summary-negative':
                        evaluated[index]['total'].isNegative
                    }"
                  >
                    {{ institution.scores.total }}/{{ categoryTotal.max_score }}
                  </span>
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
    neutralThreshold: Number,
    positiveThreshold: Number
  },

  data () {
    return {};
  },

  computed: {
    categoryTotal: function () {
      return {
        slug: 'total',
        max_score: this.categories.reduce(
          (prev, curr) => ({max_score: prev.max_score + curr.max_score})
        ).max_score
      };
    },
    evaluated: function () {
      let items = [];
      
      for (var institution of this.institutions) {
        const evals = {};

        for (var category of [...this.categories, this.categoryTotal]) {
          const percentage = 
            institution.scores[category.slug] * 100 / category.max_score;
          const isPositive = percentage >= this.positiveThreshold;
          const isNeutral = !isPositive && percentage >= this.neutralThreshold;
          const isNegative = percentage < this.neutralThreshold;

          evals[category.slug] = {
            isPositive, isNeutral, isNegative
          };
        }

        items.push(evals);
      }

      return items;
    }
  },

  methods: {
    showPopup () {
      $('#comparer-popup').modal('show');
    },
  },
};
</script>
