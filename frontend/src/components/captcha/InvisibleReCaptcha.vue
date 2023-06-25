<script setup lang="ts">
/// <reference types="@/assets/components/types/captcha.d.ts" />

import { onLoaded } from "@/assets/script/utils";
import { sitekey } from "@/config/config";

onLoaded(async () => {
  const token = await grecaptcha.enterprise.execute(sitekey.login);

  console.log(token)
})
</script>
