import { token } from "@/assets/script/user";
import { state } from "@/assets/script/global";
import { watch } from "vue";

export namespace app {
  const apps: Record<string, string> = {
    fystart: "https://fystart.cn",
    fymonitor: "https://fymonitor.deeptrain.net",
    vokkot: "https://vokkot.deeptrain.net",
    lightnotes: "https://notes.lightxi.com",
  };

  export function set(): void {
    const param = new URLSearchParams(window.location.search);
    if (param.has("app")) {
      const app = param.get("app") || "";
      if (app in apps) sessionStorage.setItem("app", app);
    }
  }

  export function exec() {
    const app = apps[sessionStorage.getItem("app") || ""];
    if (app && state.value === 2) {
      sessionStorage.removeItem("app");
      window.location.href = `${app}/login?token=${token.value}`;
    }
  }

  export function guard() {
    set();
    watch(state, exec);
  }
}
