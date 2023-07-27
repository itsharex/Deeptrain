import { createApp } from "vue";
import App from "./App.vue";
import "@/config";
import router from "./router";
import ElementPlus from "element-plus";
import "element-plus/theme-chalk/dark/css-vars.css";
import "./assets/style/main.css"; /** @ts-ignore **/
import "@/assets/script/global";
import i18n from "@/i18n";


const app = createApp(App);

app
  .use(router)
  .use(ElementPlus)
  .use(i18n)
  .mount("#app");
