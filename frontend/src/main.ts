import { createApp } from "vue";
import App from "./App.vue";
import "@/config";
import router from "./router";
import ElementPlus from "element-plus";
import "element-plus/theme-chalk/dark/css-vars.css";
import "./assets/style/main.css"; /** @ts-ignore **/
import "@/assets/script/global";


const app = createApp(App);

app.use(router).use(ElementPlus).mount("#app");
