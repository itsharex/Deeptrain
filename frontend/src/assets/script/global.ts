import '@/assets/script/user';
import { ref } from "vue";
import axios from "axios";

export const state = ref(-1);
window.addEventListener('load', async () => {
  const res = await axios.get("state");
  state.value = res.data.state;
})
