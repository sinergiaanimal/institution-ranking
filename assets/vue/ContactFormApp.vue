<template>
  <form novalidate
        @submit.prevent="sendMessage()">
    <div class="form-group">
      <label for="sender_name">{{ cfg.nameFName }}</label>
      <input type="text"
             class="form-control form-input"
             id="sender_name"
             :placeholder="cfg.namePlaceholder"
             v-model="formData.sender_name" />
      <div v-if="errors.sender_name"
           class="alert alert-danger mt-2" role="alert">
        {{ errors.sender_name.join('; ') }}
      </div>
    </div>
    <div class="form-group">
      <label for="sender_email">{{ cfg.emailFName }}</label>
      <input type="email"
             class="form-control form-input"
             id="sender_email" 
             :placeholder="cfg.emailPlaceholder"
             v-model="formData.sender_email" />
      <div v-if="errors.sender_email"
           class="alert alert-danger mt-2" role="alert">
        {{ errors.sender_email.join('; ') }}
      </div>
    </div>
    <div class="form-group">
      <label for="message">{{ cfg.messageFName }}</label>
      <textarea class="form-control form-input"
                id="sender_message"
                rows="9"
                :placeholder="cfg.messagePlaceholder"
                v-model="formData.message">
      </textarea>
      <div v-if="errors.message"
           class="alert alert-danger mt-2" role="alert">
        {{ errors.message.join('; ') }}
      </div>
    </div>
    <div v-show="showSuccessMsg"
         class="alert alert-success mt-2 mb-2" role="alert">
      Your message has been sent. Thank you for your feedback!
    </div>
    <button type="submit"
            class="button button--primary mt-3"
            :disabled="isProcessing">
      {{ cfg.buttonText }}
    </button>
    <div v-show="isProcessing"
         class="spinner-border text-warning ml-5" role="status">
      <span class="sr-only">Loading...</span>
    </div>
  </form>
</template>


<script>
import axios from 'axios';
import { apiUrls } from './static_data';

export default {
  name: 'ContactFormApp',
  
  props: {
    cfg: {
      type: Object,
      required: true,
    },
  },

  data () {
    return {
      formData: {
        plugin: this.cfg.pluginId,
        sender_name: '',
        sender_email: '',
        message: '',
      },
      errors: {},
      isProcessing: false,
      showSuccessMsg: false
    };
  },

  methods: {
    async sendMessage () {
      this.isProcessing = true;
      this.showSuccessMsg = false;
      this.errors = {};

      try {
        await axios.post(
          `${apiUrls.contactMessage}`,
          this.formData,
          {headers: {'X-CSRFToken': this.cfg.csrfToken}}
        ).then(
          (response) => {
            if (
              response.status !== 201 ||
              !response.data ||
              !response.data.status_str ||
              response.data.status_str !== 'sent'
            ) {
              alert('Something went wrong! Please contact the administrator.');
            }

            this.formData.sender_name = '';
            this.formData.sender_email = '';
            this.formData.message = '';
            this.isProcessing = false;
            this.showSuccessMsg = true;
          }
        );
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.errors = error.response.data;
        } else {
          alert('Something went wrong! Please contact the administrator.');
        }
        this.isProcessing = false;
      }
    }
  }
};
</script>
