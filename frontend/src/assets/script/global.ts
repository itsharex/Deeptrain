import '@/assets/script/user';
import { onMounted, ref } from "vue";
import axios from "axios";

const state = ref(-1);
window.addEventListener('load', async () => {
  const res = await axios.get("state");
  state.value = res.data.state;
})
