import '@/assets/script/user';
import { ref } from "vue";
import axios from "axios";
import router from "@/router";

export const state = ref(-1);
window.addEventListener('load', async () => {
  const res = await axios.get("state");
  state.value = res.data.state;
  if (state.value === 1) await router.push('/verify');
})
