import type { Ref } from "vue";
import { onMounted, watch } from "vue";
import type { FormInstance } from "element-plus";
import { language } from "@/config";

function convertNode(el: Ref<HTMLElement> | HTMLElement): HTMLElement {
  return el instanceof HTMLElement ? el : el.value;
}
export function insertScript(
  src: string,
  el: Ref<HTMLElement> | HTMLElement,
  async: boolean = false,
  defer: boolean = false,
  hook: ((this: GlobalEventHandlers, event: Event) => any) | null = null
): HTMLScriptElement {
  let script = document.createElement("script");
  script.src = src;
  script.async = async;
  script.defer = defer;
  convertNode(el).appendChild(script);
  script.onload = hook;
  return script;
}

export function insertScriptExceptExists(
  val: string,
  src: string,
  el: Ref<HTMLElement> | HTMLElement,
  async: boolean = false,
  defer: boolean = false,
  hook: ((this: GlobalEventHandlers, event: Event) => any) | null = null
): HTMLScriptElement | undefined {
  if (!(val in window)) return insertScript(src, el, async, defer, hook);
}

export function insertScriptHook(
  val: string,
  src: string,
  el: Ref<HTMLElement> | HTMLElement,
  async: boolean = false,
  defer: boolean = false,
  hook: ((...arg: any[]) => any) | null = null
): void {
  val in window ? hook?.() : insertScript(src, el, async, defer, hook);
}

export function redirect(href: string) {
  /**  Hide URL.  **/
  return (window.location.href = href);
}

export function onLoaded(callback: () => void): void {
  if (document.readyState === "complete") onMounted(callback);
  window.addEventListener("load", callback);
}

export async function validateForm(
  form: FormInstance | undefined
): Promise<boolean> {
  if (!form) return false;
  return new Promise((resolve) => {
    form.validate((valid) => resolve(valid));
  });
}

export function syncRefs(target: Ref<any>, source: Ref<any>) {
  target.value = source.value;
  watch(source, (val) => (target.value = val));
}

export function syncLangRef(locale: Ref<string>) {
  syncRefs(locale, language);
}

export function copyClipboard(text: string) {
  if (!navigator.clipboard) {
    const input = document.createElement("input");
    input.value = text;
    document.body.appendChild(input);
    input.select();
    document.execCommand("copy");
    document.body.removeChild(input);
  } else {
    navigator.clipboard.writeText(text);
  }
}
