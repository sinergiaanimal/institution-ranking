import 'bootstrap';

import { createApp } from 'vue';
import RankingBrowserApp from './vue/RankingBrowserApp.vue';
import vueDebounce from 'vue-debounce';


window.onload = function () {
    for (const elem of document.querySelectorAll('[id^=ranking-browser-app]')) {
        const idSuffix = elem.id.replace('ranking-browser-app-', '');
        const cfgElem = document.querySelector(`[id^=ranking-browser-cfg-${idSuffix}`);
        const cfgData = JSON.parse(cfgElem.innerHTML);

        createApp(RankingBrowserApp, {cfg: cfgData}).use(vueDebounce).mount(elem);
    }
};
