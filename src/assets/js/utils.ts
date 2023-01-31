import { getCurrentInstance } from "vue";
import type { Ref } from "vue";

export const properties: any = getCurrentInstance()?.appContext.config.globalProperties;

function convertNode(el: Ref<HTMLElement> | HTMLElement): HTMLElement {
  return el instanceof HTMLElement ? el : el.value;
}
export function insertScript(src: string, el: Ref<HTMLElement> | HTMLElement, async: boolean = false, defer: boolean = false): HTMLScriptElement {
  let script = document.createElement("script");
  script.src = src;
  script.async = async;
  script.defer = defer;
  convertNode(el).appendChild(script);
  return script;
}
