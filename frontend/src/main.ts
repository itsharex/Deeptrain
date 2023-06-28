import { createApp } from 'vue';
import App from './App.vue';
import { backend_url } from "@/config/config";
import router from './router';
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/dark/css-vars.css';
import './assets/sytle/main.css'; /** @ts-ignore **/
import AOS from 'aos';
import '@/assets/script/global';
import 'aos/dist/aos.css';
import axios from "axios";

AOS.init({ duration: 1000 });

const app = createApp(App);
axios.defaults.baseURL = backend_url;

app.use(router)
   .use(ElementPlus)
   .mount('#app');
