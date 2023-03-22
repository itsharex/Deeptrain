import type { Ref } from "vue";

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

export function insertScriptHook(val: string, src: string, el: Ref<HTMLElement> | HTMLElement,
                                         async: boolean = false, defer: boolean = false,
                                         hook: ((...arg: any[]) => any) | null = null
): void {
  ( val in window ) ? hook?.() : insertScript(
    src, el, async, defer, hook,
  );
}

export function redirect(href: string) {
  /**  Hide URL.  **/
  return window.location.href = href;
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