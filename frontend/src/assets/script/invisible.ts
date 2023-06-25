import { sitekey } from "@/config/config";

export async function performCheck(e: Event) {
  e.preventDefault();
  grecaptcha.enterprise.ready(async () => {
    const token = await grecaptcha.enterprise.execute(sitekey.login);
    console.log(token)
  });
}
