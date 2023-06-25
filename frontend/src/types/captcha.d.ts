declare namespace grecaptcha {
  namespace enterprise {
    function ready(hook: () => any): void;
    function reset(id?: string): void;
    function render(id: string, options: {
      sitekey: string,
      size?: string,
      theme?: string,
      callback?: (response: string) => any,
    }): void;

    async function execute(sitekey: string, options?: {
      action?: string,
    }): Promise<string>;
  }
}
