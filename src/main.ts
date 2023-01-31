import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/dark/css-vars.css';
import './assets/css/main.css'; /** @ts-ignore **/
import AOS from 'aos';
import 'aos/dist/aos.css';

AOS.init({ duration: 1000 });

const app = createApp(App);

app.config.globalProperties.$hcaptcha = '10000000-ffff-ffff-ffff-000000000001';
app.config.globalProperties.$turnstile = '1x00000000000000000000AA';

app.use(router)
   .use(ElementPlus)
   .mount('#app');
