<script setup lang="ts">
import { insertScriptExceptExists } from "@/assets/js/utils";
import { turnstile_sitekey } from "@/config/config";
import { onMounted, ref } from "vue";
import type { Ref } from "vue";

const props = defineProps<{
  id: string,
  theme?: string,
}>();
const emit = defineEmits(["update:modelValue"]);

const field: Ref<any> = ref();
onMounted(() => {
  insertScriptExceptExists(
    'turnstile', "https://challenges.cloudflare.com/turnstile/v0/api.js", field,
    true, true,
    (): void => {   /** @ts-ignore **/
    const turnstile = window.turnstile;
      turnstile.render(field.value, {
        sitekey: turnstile_sitekey,
        theme: props.theme || "dark",
        callback: (val: string): void => (
          emit("update:modelValue", val)
        ),
      });
    }
  )
});

</script>
<template>
  <div ref="field" class="cf-captcha" :id="id" />
</template>

<style scoped>
.cf-captcha {
  margin-top: 2px;
}
</style>