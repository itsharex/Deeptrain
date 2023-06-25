declare namespace grecaptcha {
  namespace enterprise {
    function render(id: string, options: {
      sitekey: string,
      size?: string,
      theme?: string,
      callback?: (response: string) => any,
    });
  }
}


declare namespace turnstile {
  function render(element: HTMLElement | string, options: {
    sitekey: string,
    size?: string,
    theme?: string,
    callback?: (response: string) => any,
  });
}
