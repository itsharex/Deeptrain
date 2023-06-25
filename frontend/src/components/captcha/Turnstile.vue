<script setup lang="ts">
/// <reference types="@/assets/components/types/captcha.d.ts" />

import { sitekey } from "@/config/config";
import { onMounted, ref } from "vue";

const props = defineProps<{
  id: string,
  size?: string,
  theme?: string,
}>();
const emit = defineEmits(["update:modelValue"]);

const field = ref<HTMLElement>();
window.addEventListener('load', () => {
  if (field.value) turnstile.render(props.id, {
    sitekey: sitekey.turnstile,
    size: props.size || "normal",
    theme: props.theme || "dark",
    callback: (val: string): void => emit("update:modelValue", val),
  });
});
</script>

<template>
  <div class="cf-captcha" :id="id" />
</template>

<style scoped>
.cf-captcha {
  margin: 2px auto 0;
}
</style>
