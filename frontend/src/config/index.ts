import axios from "axios";

export const deploy: boolean = true;
export let backend_url: string = 'http://localhost:8080/';
if (deploy) backend_url = 'https://api.deeptrain.net/';

export namespace sitekey {
  export const recaptcha: string = "6Ld7I8gmAAAAACiyFPXekOJTP3skNBDOU5934ULn";
  export const geetest: string = "cfea99009bc22a958bf3bff2f3a06a8f";
}

axios.defaults.baseURL = backend_url;
