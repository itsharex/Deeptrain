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
  initGeetest4(
    {
      captchaId: sitekey.geetest,
      product: "bind",
      hideSuccess: true,
    },
    function (captcha: Geetest.Geetest) {
      captcha.appendTo(`#${props.id}`);
      emit("update:modelValue", captcha);
      captcha.onFail(captcha.reset);
      captcha.onError(captcha.reset);
    }
  );
});
</script>

<template>
  <div ref="field" class="geetest" :id="id" />
</template>

<style></style>
