<script setup lang="ts">
import { insertScriptExceptExists, properties } from "@/assets/js/utils";
import { onMounted, ref } from "vue";
import type { Ref } from "vue";

const field: Ref<any> = ref();
defineProps<{
  key?: string,
  theme?: string,
}>();
onMounted(() => {
  insertScriptExceptExists(
    'hcaptcha', "https://hcaptcha.com/1/api.js", field,
    true, true,
    console.log,
  )
});

function getCaptcha(): string {
  // @ts-ignore
  return exist() ? hcaptcha.getResponse() : ""
}
</script>
<template>
<div ref="field">
  <div class="h-captcha"
       required
       :data-sitekey="properties.$hcaptcha"
       :data-theme="theme ? theme : 'light'"
       data-callback="func_local"
  ></div>
</div>
</template>
