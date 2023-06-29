export namespace app {
  const apps: Record<string, string> = {
    "fystart": "https://fystart.deeptrain.net/",
    "fymonitor": "https://fymonitor.deeptrain.net/",
    "vokkot": "https://vokkot.deeptrain.net/",
  }

  export function set(app: string): void {
    const param = new URLSearchParams(window.location.search);
    if (param.has("app")) app = param.get("app") || "";
    if (app in apps) sessionStorage.setItem("app", app);
  }

  export function get(): string | undefined {
    return apps[sessionStorage.getItem("app") || ""];
  }

  export function clear(): void {
    sessionStorage.removeItem("app");
  }

  export function exec() {
    const app = get();
    if (app) {
      clear();
      window.location.href = app;
    }
  }
}
