import '@/assets/script/user';
import { ref } from "vue";
import axios from "axios";
import router from "@/router";
import { token } from "@/assets/script/user";

export const state = ref(-1);
window.addEventListener('load', refreshState);

export function refreshState(option?: any) {
  if (token.value === "") return state.value = 0;
  axios.get("state").then(res => {
    state.value = res.data.status;
    if (typeof option == "object" && typeof option.callback == "function") option.callback(state.value);
    if (state.value === 1) router.push('/verify').then(() => 0);
  })
}

export function blockUtilSetup(): Promise<void> {
  if (state.value === -1) return new Promise<void>(resolve => {
    let interval = setInterval(() => {
      if (state.value !== -1) {
        clearInterval(interval);
        resolve();
      }
    }, 100);
  });
  else return Promise.resolve();
}
