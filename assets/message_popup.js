import 'bootstrap/js/dist/modal';

import { createApp } from 'vue';
import MessagePopupApp from './vue/MessagePopupApp.vue';


window.onload = function () {
  const elem = document.querySelector('[id=message-popup-app]');
  const cfgElem = document.querySelector('[id=message-popup-cfg]');
  const cfgData = JSON.parse(cfgElem.innerHTML);

  createApp(MessagePopupApp, { cfg: cfgData }).mount(elem);
};
