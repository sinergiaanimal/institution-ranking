<template>
  <div id="message-popup" class="modal fade popup" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title popup__title">
            Sending a message to
            <i>{{ institution.name }}</i>
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
          <div v-for="message in messages" :key="message.id">
            <p
              v-if="message.kind == messageTemplateKind.GOOD"
              class="popup__message popup__message--good"
            >
              Express your gratitude to
              <span class="popup__institution-name">{{
                institution.name
              }}</span>
              for animals-oriented policies
              <i class="far fa-smile"></i>
            </p>
            <p
              v-else-if="message.kind == messageTemplateKind.BAD"
              class="popup__message popup__message--bad"
            >
              Express your concern to
              <span class="popup__institution-name">{{
                institution.name
              }}</span>
              for lack of animals-oriented policies
              <i class="far fa-frown"></i>
            </p>

            <p :id="'message-' + message.id"
               class="popup__message popup__message--content">
              {{ message.content }}
              <transition name="fade">
                <div class="popup__copy-msg" v-show="showCopyInfo">
                  Message has been copied to the clipboard.
                </div>
              </transition>
              <button
                type="button"
                class="icon icon--copy popup__copy-btn"
                title="Copy message to the clipboard"
                @click="copyToClipboard(message.content)"
              >
                <span class="sr-only">Copy to clipboard</span>
              </button>
            </p>
          </div>

          <h2 class="popup__subtitle">
            Choose a way of contact with
            <i>{{ institution.name }}</i>
          </h2>
          <div 
            v-if="institutionDetail"
            class="d-flex justify-content-center mb-3"
          >
            <a
              v-for="email in institutionDetail.emails"
              :key="email.id"
              class="icon icon--spaced icon--mail"
              :href="'mailto:' + email.address"
              :title="'E-mail: ' + email.address"
            >
            </a>
            <div
              v-for="sm in institutionDetail.social_media_links"
              :key="sm.id"
            >
              <a
                :class="[
                  'icon',
                  'icon--spaced',
                  'icon--' + sm.kind_name.toLowerCase(),
                ]"
                :href="sm.url"
                target="_blank"
                rel="noopener noreferrer"
                :title="sm.kind_name + ': ' + sm.url"
              >
                <span class="sr-only">{{ sm.kind_name }}</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import $ from 'jquery';

import { apiUrls, messageTemplateKind } from './static_data';

export default {
  data () {
    return {
      policyCategories: null,
      messageTemplates: [],
      institution: { scores: {} },
      institutionDetail: null,
      messages: [],
      messageTemplateKind: messageTemplateKind,
      showCopyInfo: false
    };
  },

  methods: {
    showMessagePopup (institution) {
      this.institution = institution;
      this.messages = this.getMessages(institution);
      this.getInstitutionDetail(this.institution.id);

      $('#message-popup').modal('show');
    },

    getMessageTemplates () {
      axios.get(apiUrls.messageTemplates).then((response) => {
        this.messageTemplates = response.data;
      });
    },

    getMessages (institution) {
      return this.messageTemplates.filter((item) => {
        return (
          (item.min_score === null ||
            institution.scores.total >= item.min_score) &&
          (item.max_score === null ||
            institution.scores.total <= item.max_score)
        );
      });
    },

    getInstitutionDetail (institutionId) {
      axios.get(`${apiUrls.institutions}${institutionId}/`).then((response) => {
        this.institutionDetail = response.data;
      });
    },

    copyToClipboard (content) {
      function listener (e) {
        e.clipboardData.setData('text/html', content);
        e.clipboardData.setData('text/plain', content);
        e.preventDefault();
      }
      document.addEventListener('copy', listener);
      document.execCommand('copy');
      document.removeEventListener('copy', listener);

      this.showCopyInfo = true;
      setTimeout(() => { this.showCopyInfo = false; }, 2000);
    },
  },

  mounted () {
    this.getMessageTemplates();
  },
};
</script>
