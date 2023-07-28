import type { Ref } from "vue";
import { watch, ref } from "vue";
import axios from "axios";
import type { ComposerTranslation } from "vue-i18n";

export const token: Ref<string> = ref(localStorage.getItem("token") || "");
axios.defaults.headers.common["Authorization"] = token.value;
watch(token, () => {
  const _token = token.value;
  localStorage.setItem("token", _token);
  axios.defaults.headers.common["Authorization"] = _token;
});

const mailSuffixes: string[] = [
  "gmail.com",
  "outlook.com",
  "163.com",
  "qq.com",
  "deeptrain.net",
];

const isCommonEmailSuffix = (suffix: string): boolean => {
  for (const _suffix of mailSuffixes) if (suffix === _suffix) return true;
  return false;
};

export const validateEmail = function (t: ComposerTranslation) {
  return (rules: any, value: any, callback: any): void => {
    const res: string[] = value.trim().split("@");
    if (res.length !== 2 || res.some((n) => !n))
      return callback(t("user.email-format-error"));
    const [mail, suffix] = res;
    if (!/^\S+$/.test(mail)) return callback(t("user.email-format-error"));
    if (!isCommonEmailSuffix(suffix))
      return callback(t("user.email-format-unsupported"));
    callback();
  };
};

export function validateRePassword(
  t: ComposerTranslation,
  form: Record<string, any>,
  field?: string
): (rules: any, value: any, callback: any) => void {
  return (rules: any, value: any, callback: any): any =>
    form[field || "password"] !== value
      ? callback(t("user.rule-password-not-same"))
      : callback();
}

export function validateChangePassword(
  t: ComposerTranslation,
  form: Record<string, any>
) {
  return (rules: any, value: any, callback: any): any =>
    form.old_password === value
      ? callback(t("user.rule-password-not-different"))
      : callback();
}
