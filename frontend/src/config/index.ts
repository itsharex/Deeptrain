import axios from "axios";
import { ref, watch } from "vue";

export const deploy: boolean = true;
export const token_field = deploy ? "token" : "token_dev";

export const supportLanguages = ["zh", "en"];
export const language = ref(getLanguage());
export let backend_url: string = "http://localhost:8080/";
export let callback_url: string = "http://localhost:5173/";
if (deploy) {
  backend_url = "https://api.deeptrain.net/";
  callback_url = "https://deeptrain.net/";
}

function getLanguage() {
  const lang: string = localStorage.getItem("language") || navigator.language.slice(0, 2) || "zh";
  if (supportLanguages.includes(lang)) return lang;
  return "zh";
}

watch(language, () => localStorage.setItem("language", language.value));

export namespace sitekey {
  export const recaptcha: string = "6Ld7I8gmAAAAACiyFPXekOJTP3skNBDOU5934ULn";
  export const geetest: string = "cfea99009bc22a958bf3bff2f3a06a8f";
}

export namespace oauth {
  export const github: string = "5d47a861704423cb30a9";
  export const google: string =
    "767514888852-vvtu4bve0l5u98klpofcliod33lug6fh.apps.googleusercontent.com";

  export const github_url: string = `https://github.com/login/oauth/authorize?scope=user:email&client_id=${github}`;
  export const google_url: string = `https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=${callback_url}oauth/google&response_type=code&scope=https://www.googleapis.com/auth/userinfo.email&client_id=${google}`;
}

axios.defaults.baseURL = backend_url;
