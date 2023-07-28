import axios from "axios";
import { ref, watch } from "vue";

export const deploy: boolean = true;
export const language = ref(localStorage.getItem("language") || "zh");
export let backend_url: string = "http://localhost:8080/";
if (deploy) backend_url = "https://api.deeptrain.net/";

watch(language, () => localStorage.setItem("language", language.value));

export namespace sitekey {
  export const recaptcha: string = "6Ld7I8gmAAAAACiyFPXekOJTP3skNBDOU5934ULn";
  export const geetest: string = "cfea99009bc22a958bf3bff2f3a06a8f";
}

export namespace oauth {
  export const github: string = "5d47a861704423cb30a9";
}

axios.defaults.baseURL = backend_url;
