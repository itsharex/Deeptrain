<script setup lang="ts">
/// <reference types="@/assets/components/types/captcha.d.ts" />

import { sitekey } from "@/config/config";
import { ref } from "vue";

const props = defineProps<{
  id: string,
  size?: string,
  theme?: string,
}>();
const emit = defineEmits(["update:modelValue"]);

const field = ref<any>();
window.addEventListener('load', () => {
  grecaptcha.enterprise.render(props.id, {
    sitekey: sitekey.recaptcha,
    size: props.size || "normal",
    theme: props.theme || "light",
    callback: (val: string): void => emit("update:modelValue", val),
  });
});

</script>
<template>
  <div ref="field" class="recaptcha" :id="id" />
</template>

<style scoped>
.recaptcha {
  margin: 2px auto 0;
}
</style>
