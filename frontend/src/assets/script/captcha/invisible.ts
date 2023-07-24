import { sitekey } from "@/config";

export async function performCheck(e: Event): Promise<string> {
  e.preventDefault();
  return new Promise((resolve) =>
    grecaptcha.enterprise.ready(async () => {
      const token: string = await grecaptcha.enterprise.execute(
        sitekey.geetest,
        { action: "login" }
      );
      resolve(token);
    })
  );
}
