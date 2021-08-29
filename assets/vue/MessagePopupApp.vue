<template>
  <div>
    <button type="button" class="button button--primary mt-5 mb-5"
            @click="showMessagePopup()">
      {{ cfg.buttonTitle }}
    </button>

    <MessagePopup ref="messagePopup" />
  </div>
</template>


<script>
import MessagePopup from './MessagePopup.vue';

export default {
  name: 'MessagePopupApp',
  
  components: {
    MessagePopup,
  },
  
  props: {
    cfg: {
      type: Object,
      required: true,
    },
  },

  methods: {
    showMessagePopup () {
      this.$refs.messagePopup.showMessagePopup(this.cfg.institution);
    }
  }
};
</script>