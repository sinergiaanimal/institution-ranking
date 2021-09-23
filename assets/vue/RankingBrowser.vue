<template>
  <section>
    <div class="d-flex flex-column flex-md-row justify-content-between mb-3">
      <div class="form-group d-flex">
        <input
          class="input input--search"
          type="text"
          placeholder="SEARCH"
          v-debounce:300ms="applySearch"
        />
        <i class="
          fas fa-search fa-2x d-inline-block color-neutral-20 mt-2 ml-3
        "></i>
      </div>
      <button
        type="button"
        class="button button--primary mb-3"
        @click="switchComparisonMode()"
      >
        <span v-if="comparisonMode">STOP COMPARING</span>
        <span v-else>
          {{ cfg.compareBtnText }}
        </span>
      </button>
    </div>

    <div class="browser-table">
      <table class="table">
        <thead>
          <tr>
            <th
              scope="col"
              class="sticky-md"
              v-show="comparisonMode">
            </th>

            <ColumnHeader
              :col-name="'name'"
              :col-title="cfg.instColName"
              :ordering-array="ordering"
              :extra-classes="{
                'sticky-md': true,
                'sticky-md-offset': comparisonMode
              }"
              @ordering-changed="onOrderingChanged"
            />

            <ColumnHeader
              :col-name="'score_total'"
              col-title="Score"
              :ordering-array="ordering"
              @ordering-changed="onOrderingChanged"
              :tooltip="'Maximum total score is ' + maxScore + ' points'"
            />

            <ColumnHeader
              :col-name="'country'"
              col-title="Country"
              :ordering-array="ordering"
              @ordering-changed="onOrderingChanged"
            />

            <ColumnHeader
              v-for="category in policyCategories"
              class="text-center"
              :key="category.id"
              :col-name="'score_' + category.slug"
              :col-title="category.short_name"
              :extra-classes="'policy-cat-col'"
              :ordering-array="ordering"
              :tooltip="
                category.name + ' | Max score: ' +
                category.max_score + ' points'
              "
              @ordering-changed="onOrderingChanged"
            />

            <th scope="col" :class="{'d-none': comparisonMode}">Action</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="institution in institutions"
              :key="institution.id"
              :set="scorePercentage = Math.round(
                (100 * institution.scores.total) / maxScore
              )"
              :class="{'row-selected': selection.includes(institution)}">
            <td v-show="comparisonMode" class="sticky-md">
              <div class="mt-1">
                <input
                  type="checkbox"
                  class="input table-institution-checkbox-input"
                  @change="updateSelection(institution, $event)"
                  :disabled="
                    selectionLimitReached && !selection.includes(institution)
                  "
                />
              </div>
            </td>
            <td
              :class="{
                'sticky-md': true,
                'sticky-md-offset': comparisonMode
              }"
            >
              <a
                :href="detailsPageUrl + institution.slug + '/'"
                class="d-flex align-items-center"
              >
                <figure
                  :style="{
                    'background-image':
                      'url(' + (
                        institution.logo_thumb || defaultThumbUrl
                      ) + ')',
                  }"
                  class="institution-thumb"
                ></figure>
                {{ institution.name }}
              </a>
            </td>
            <td>
              <div
                class="progress progress--gold"
                :title="'score: ' + institution.scores.total + '/' + maxScore"
              >
                <div class="progress-value">
                  {{ scorePercentage }}%
                </div>
                <div
                  class="progress-bar"
                  role="progressbar"
                  :style="
                    'width: ' + scorePercentage + '%'
                  "
                  :aria-valuenow="institution.scores.total"
                  aria-valuemin="0"
                  :aria-valuemax="maxScore"
                >
                </div>
              </div>
            </td>
            <td>{{ institution.country }}</td>

            <td
              scope="col"
              v-for="category in policyCategories"
              class="text-center"
              :key="category.id"
            >
              {{ institution.scores[category.slug] + '/' + category.max_score }}
            </td>

            <td scope="col"
                :class="{'d-none': comparisonMode}">
              <i class="far fa-envelope fa-lg
                        d-block text-center color-primary-60 cursor-pointer"
                @click="showMessagePopup(institution)">
              </i>
            </td>
          </tr>
          <tr v-if="!(institutions && institutions.length)">
            <td colspan="100" class="no-results-col">
              No results
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <MessagePopup ref="messagePopup" />

    <ComparerPopup
      ref="comparerPopup"
      :popup-title="cfg.popupTitle"
      :popup-info="popupInfo"
      :categories="policyCategories"
      :institutions="selection"
      :neutralThreshold="cfg.neutralThreshold"
      :positiveThreshold="cfg.positiveThreshold"
    />
  </section>
</template>

<script>
import axios from 'axios';
import ColumnHeader from './ColumnHeader.vue';
import MessagePopup from './MessagePopup.vue';
import ComparerPopup from './ComparerPopup.vue';

import { apiUrls } from './static_data';

export default {
  components: {
    ColumnHeader,
    MessagePopup,
    ComparerPopup,
  },

  props: {
    cfg: {
      type: Object,
      required: true,
    },
  },

  data () {
    return {
      defaultThumbUrl: '/static/comparer/img/institution-logo-default.svg',
      detailsPageUrl: '/institutions/',
      policyCategories: null,
      maxScore: null,
      institutions: null,
      ordering: this.cfg.orderBy
        ? this.cfg.orderBy.split(',')
        : ['-score_total'],
      popupInfo: this.cfg.popupInfo.replace(
        '<counter>',
        `${this.cfg.selectionLimit}`
      ),
      searchText: '',
      selection: [],
      selectionLimit: this.cfg.selectionLimit,
      comparisonMode: false,
    };
  },

  computed: {
    selectionLimitReached: function () {
      return this.selection.length >= this.selectionLimit;
    },
  },

  methods: {
    onOrderingChanged (colName) {
      const colIndex = this.ordering.indexOf(colName);
      const colRevIndex = this.ordering.indexOf(`-${colName}`);

      if (colIndex >= 0) {
        this.ordering[colIndex] = `-${colName}`; // reverse ordering
      } else if (colRevIndex >= 0) {
        if (this.ordering.length > this.cfg.minOrderBy) {
          this.ordering.splice(colRevIndex, 1); // remove ordering
        } else {
          // reverse instead of removing if min limit is reached
          this.ordering[colRevIndex] = `${colName}`;
        }
      } else {
        if (this.ordering.length >= this.cfg.maxOrderBy) {
          // remove the first current ordering option if max limit is reached
          this.ordering.shift();
        }
        this.ordering.push(colName); // add ordering
      }

      this.getInstitutionList();
    },

    updateSelection (institution, event) {
      if (event.target.checked) {
        this.selection.push(institution);
      } else {
        this.selection.splice(this.selection.indexOf(institution), 1);
      }
    },

    getInstitutionList () {
      if (this.comparisonMode) {
        // Turn off comparison mode if institution list is going to change.
        this.switchComparisonMode();
      }

      axios.get(apiUrls.policyCategories).then((response) => {
        let getParams = {
          ordering: `${this.ordering.join(',')}`,
        };

        this.policyCategories = response.data;

        this.maxScore = 0;
        for (const cat of this.policyCategories) {
          this.maxScore += cat.max_score;
        }

        if (this.searchText) {
          getParams.search = `${this.searchText}`;
        }

        axios
          .get(`${apiUrls.institutions}`, { params: getParams })
          .then((response) => (this.institutions = response.data));
      });
    },

    applySearch (val, _event) {
      this.searchText = val;
      this.getInstitutionList();
    },

    showMessagePopup (institution) {
      this.$refs.messagePopup.showMessagePopup(institution);
    },

    switchComparisonMode () {
      this.comparisonMode = !this.comparisonMode;

      if (!this.comparisonMode) {
        this.selection = [];
        document
          .querySelectorAll('.table-institution-checkbox-input')
          .forEach((element) => {
            element.checked = false;
          });
      }
    },
  },

  mounted () {
    this.getInstitutionList();
  },
};
</script>
