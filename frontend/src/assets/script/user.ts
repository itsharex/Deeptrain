import type { Ref } from "vue";
import { watch, ref } from "vue";
import axios from "axios";

export const captchaSize: string = ( document.body.offsetWidth <= 390 ) ? "compact" : "normal";
export const token: Ref<string> = ref(localStorage.getItem("token") || "");

watch(token, () => {
  localStorage.setItem("token", token.value);
  axios.defaults.headers.common["Authorization"] = token.value;
});

const mailSuffixes: string[] = [
  "gmail.com",
  "outlook.com",
  "163.com",
  "qq.com",
  "deeptrain.net",
]

const isCommonEmailSuffix = (suffix: string): boolean => {
  for (const _suffix of mailSuffixes) if (suffix === _suffix) return true; return false;
}

export const validateEmail = (rules: any, value: any, callback: any): void => {
  const res: string[] = value.trim().split("@");
  if ((res.length !== 2) || (res.some(n => ! n))) return callback("The format of the email is incorrect");
  const [mail, suffix] = res; if (!(/^\S+$/.test(mail))) return callback("The format of the email is incorrect");
  if (!(isCommonEmailSuffix(suffix))) return callback("Please use a supported email suffix");
  callback();
}

export function validateRePassword(form: { password: string }): (rules: any, value: any, callback : any) => void  {
  return (rules: any, value: any, callback : any): any =>
    (form.password !== value) ?
      callback("The password does not match") :
      callback();
}
