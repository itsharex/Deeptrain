import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/dark/css-vars.css';
import './assets/main.css'; /** @ts-ignore **/
import AOS from 'aos';
import 'aos/dist/aos.css';


AOS.init({ duration: 1000 });
const app = createApp(App);

app.use(router).use(ElementPlus);

app.mount('#app');
