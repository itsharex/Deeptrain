<script setup lang="ts">
import { sitekey } from "@/config";
import { ref } from "vue";
import { onLoaded } from "@/assets/script/utils";

const props = defineProps<{
  id: string;
  size?: string;
  theme?: string;
}>();
const emit = defineEmits(["update:modelValue"]);

const field = ref<any>();

onLoaded(() => {
  grecaptcha.enterprise.render(props.id, {
    sitekey: sitekey.recaptcha,
    size: props.size || "normal",
    theme: props.theme || "dark",
    callback: (val: string): void => emit("update:modelValue", val),
  });
});
</script>

<template>
  <div ref="field" class="recaptcha" :id="id" />
</template>

<style>
.recaptcha {
  margin: 2px auto 4px;
}

.recaptcha div {
  border-bottom: 1px solid #525252;
  border-radius: 6px;
  overflow: hidden;
  width: 301px !important;
  height: 75px !important;
}

@media (max-width: 390px) {
  .recaptcha div {
    border-right: 1px solid #525252;
    width: 157px !important;
    height: 137px !important;
  }
}
</style>
