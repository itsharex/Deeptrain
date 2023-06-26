import { sitekey } from "@/config/config";

export async function performCheck(e: Event): Promise<string> {
  e.preventDefault();
  return new Promise(resolve => grecaptcha.enterprise.ready(
    async () => {
      const token: string = await grecaptcha.enterprise.execute(
        sitekey.login,
        { action: 'login' },
      );
      resolve(token);
    }
  ))
}
