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


declare namespace Geetest {
  type Product = 'float' | 'popup' | 'bind';

  interface NativeButton {
    width?: string;
    height?: string;
  }

  interface Mask {
    outside?: boolean;
    bgColor?: string;
  }

  type Language =
    | 'zho'
    | 'eng'
    | 'zho-tw'
    | 'zho-hk'
    | 'udm'
    | 'jpn'
    | 'ind'
    | 'kor'
    | 'rus'
    | 'ara'
    | 'spa'
    | 'pon'
    | 'por'
    | 'fra'
    | 'deu';

  type RiskType = string;

  interface GeetestOptions {
    captchaId: string;
    product?: Product;
    nativeButton?: NativeButton;
    rem?: number;
    language?: Language;
    protocol?: string;
    timeout?: number;
    hideBar?: string[];
    mask?: Mask;
    apiServers?: string[];
    nextWidth?: string;
    riskType?: RiskType;
    hideSuccess?: boolean;
    offlineCb?: () => void;
    onError?: (error: Error) => void;
    userInfo?: string;
  }

  class Geetest {
    constructor(options: GeetestOptions.GeetestOptions);

    showCaptcha(): void;
    appendTo(el: string | HTMLElement): void;
    getValidate(): Record<string, any>;
    reset(): void;
    destroy(): void;
    onReady(f: () => any): void;
    onSuccess(f: () => any): void;
    onFail(f: () => any): void;
    onError(f: () => any): void;
  }
}

function initGeetest4(option: Geetest.GeetestOptions, callback: (captcha: Geetest.Geetest) => any);
