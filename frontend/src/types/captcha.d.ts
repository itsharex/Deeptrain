declare namespace grecaptcha {
  namespace enterprise {
    function ready(hook: () => any);
    function render(id: string, options: {
      sitekey: string,
      size?: string,
      theme?: string,
      callback?: (response: string) => any,
    });

    async function execute(sitekey: string, options?: {
      action?: string,
    });
  }
}
