import { sitekey } from "@/config/config";

export async function performCheck(e: Event) {
  e.preventDefault();
  const token = await grecaptcha.enterprise.execute(sitekey.login);
  console.log(token)
}
