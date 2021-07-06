import { createApp } from 'vue';
import RankingBrowserApp from './vue/RankingBrowserApp.vue';


window.onload = function () {
    for (const elem of document.querySelectorAll('.ranking-browser-app')) {
        createApp(RankingBrowserApp).mount(elem);
    }
};
