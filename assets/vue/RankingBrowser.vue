<template>
  <section>
    <button
      type="button"
      class="btn btn-warning float-right"
      @click="switchComparisonMode()"
    >
      <span v-if="comparisonMode"> STOP COMPARING </span>
      <span v-else>
        {{ cfg.compareBtnText }}
      </span>
    </button>
    <div class="form-group" style="max-width: 50%">
      <input
        class="form-control"
        type="text"
        placeholder="Search"
        v-debounce:300ms="applySearch"
      />
    </div>
    <table class="ranking-browser-table table">
      <thead>
        <tr>
          <th scope="col" v-show="comparisonMode"></th>

          <ColumnHeader
            :col-name="'name'"
            :col-title="cfg.instColName"
            :ordering-array="ordering"
            @ordering-changed="onOrderingChanged"
          />

          <ColumnHeader
            :col-name="'score_total'"
            col-title="Score"
            :ordering-array="ordering"
            @ordering-changed="onOrderingChanged"
          />

          <ColumnHeader
            :col-name="'country'"
            col-title="Country"
            :ordering-array="ordering"
            @ordering-changed="onOrderingChanged"
          />

          <ColumnHeader
            v-for="category in policyCategories"
            :key="category.id"
            :col-name="'score_' + category.slug"
            :col-title="category.name"
            :ordering-array="ordering"
            @ordering-changed="onOrderingChanged"
          />

          <th scope="col">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="institution in institutions" :key="institution.id">
          <td v-show="comparisonMode">
            <input
              type="checkbox"
              class="table-institution-checkbox-input"
              @change="updateSelection(institution, $event)"
              :disabled="
                selectionLimitReached && !selection.includes(institution)
              "
            />
          </td>
          <td>
            <a
              :href="detailsPageUrl + institution.slug + '/'"
              class="d-flex align-items-center"
            >
              <figure
                :style="{
                  'background-image':
                    'url(' + (institution.logo_thumb || defaultThumbUrl) + ')',
                }"
                class="institution-thumb"
              ></figure>
              {{ institution.name }}
            </a>
          </td>
          <td>
            <div
              class="progress"
              :title="institution.scores.total + ' / ' + maxScore"
            >
              <div
                class="progress-bar"
                role="progressbar"
                :style="
                  'width: ' + (100 * institution.scores.total) / maxScore + '%'
                "
                :aria-valuenow="institution.scores.total"
                aria-valuemin="0"
                :aria-valuemax="maxScore"
              >
                {{ institution.scores.total }} / {{ maxScore }}
              </div>
            </div>
          </td>
          <td>{{ institution.country }}</td>

          <td
            scope="col"
            v-for="category in policyCategories"
            :key="category.id"
          >
            {{ institution.scores[category.slug] }}
          </td>

          <th scope="col">
            <i class="far fa-envelope" @click="showMessagePopup(institution)">
            </i>
          </th>
        </tr>
      </tbody>
    </table>

    <MessagePopup ref="messagePopup" />

    <ComparerPopup
      ref="comparerPopup"
      :popup-title="cfg.popupTitle"
      :popup-info="popupInfo"
      :categories="policyCategories"
      :institutions="selection"
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
        this.ordering.splice(colRevIndex, 1); // remove ordering
      } else {
        this.ordering.push(colName); // add ordering
      }

      this.getInstitutionList();
    },

    updateSelection (institution, event) {
      if (event.target.checked) {
        this.selection.push(institution);
      } else {
        this.selection.splice(this.selection.indexOf(institution));
      }
    },

    getInstitutionList () {
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
