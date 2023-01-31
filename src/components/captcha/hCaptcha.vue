<script setup lang="ts">
import { insertScript } from '@/assets/js/utils';
import { onMounted, ref } from "vue";
import type { Ref } from "vue";

const field: Ref<any> = ref();
defineProps<{
  key?: string,
  theme?: string,
}>();
onMounted(() => (
  insertScript("https://hcaptcha.com/1/api.js", field, true, true)
));

function exist(): boolean {
  return 'hcaptcha' in window;
}
function getCaptcha(): string {
  // @ts-ignore
  return exist() ? hcaptcha.getResponse() : ""
}

// @ts-ignore
window.example = console.log
</script>
<template>
<div ref="field">
  <div class="h-captcha"
       required
       :data-sitekey="key ? key : '10000000-ffff-ffff-ffff-000000000001'"
       :data-theme="theme ? theme : 'light'"
       data-callback="example"
  ></div>
</div>
</template>
