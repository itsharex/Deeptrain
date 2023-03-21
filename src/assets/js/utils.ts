import type { Ref, reactive } from "vue";

function convertNode(el: Ref<HTMLElement> | HTMLElement): HTMLElement {
  return el instanceof HTMLElement ? el : el.value;
}
export function insertScript(src: string, el: Ref<HTMLElement> | HTMLElement,
                             async: boolean = false, defer: boolean = false,
                             hook: ((this:GlobalEventHandlers, event: Event) => any) | null = null
                            ): HTMLScriptElement {
  let script = document.createElement("script");
  script.src = src;
  script.async = async;
  script.defer = defer;
  convertNode(el).appendChild(script);
  script.onload = hook;
  return script;
}

export function insertScriptExceptExists(val: string, src: string, el: Ref<HTMLElement> | HTMLElement,
                                         async: boolean = false, defer: boolean = false,
                                         hook: ((this:GlobalEventHandlers, event: Event) => any) | null = null
                                        ): HTMLScriptElement | undefined {
  if (!(val in window)) return insertScript(
    src, el, async, defer, hook,
  );
}

export const mailSuffixes: string[] = [
  "gmail.com",
  "yahoo.com",
  "163.com",
  "qq.com",
  "dingtalk.com",
]

const isCommonEmailSuffix = (suffix: string): boolean => {
  for (const _suffix of mailSuffixes) if (suffix === _suffix) return true; return false;
}

export function validateEmail(rules: any, value: any, callback: any): any {
  const res: string[] = value.trim().split("@");
  if ((res.length !== 2) || (res.some(n => ! n))) return callback(new Error("The format of the email is incorrect"));
  const [mail, suffix] = res; if (!(/^\S+$/.test(mail))) return callback(new Error("The format of the email is incorrect"));
  if (!(isCommonEmailSuffix(suffix))) return callback(new Error("Please use a supported email suffix"));
}

export function validateRePassword(form: { password: string }): (rules: any, value: any, callback : any) => any  {
  return (rules: any, value: any, callback : any): any =>
    callback(
      (form.password !== value) ? new Error("The password does not match") : undefined,
    );
}