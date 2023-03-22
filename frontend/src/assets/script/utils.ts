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
