import { createApp } from 'vue';
import ContactFormApp from './vue/ContactFormApp.vue';


window.onload = function () {
  for (const elem of document.querySelectorAll('[id^=contact-form-app]')) {
    const idSuffix = elem.id.replace('contact-form-app-', '');
    const cfgElem = document.querySelector(
      `[id^=contact-form-cfg-${idSuffix}`
    );
    const cfgData = JSON.parse(cfgElem.innerHTML);

    createApp(ContactFormApp, { cfg: cfgData }).mount(elem);
  }
};
