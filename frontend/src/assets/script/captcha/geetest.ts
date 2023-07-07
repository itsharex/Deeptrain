export function getValidateUtilSuccess(
  captcha: Geetest.Geetest | null
): Promise<Record<string, any>> {
  if (!captcha) return Promise.reject("captcha is null");
  return new Promise((resolve, reject) => {
    captcha.showCaptcha();
    captcha.onSuccess(() => resolve(captcha.getValidate()));
  });
}
