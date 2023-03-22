<script setup lang="ts">
import { insertScriptHook } from "@/assets/script/utils";
import { hcaptcha_sitekey } from "@/config/config";
import { onMounted, ref } from "vue";

const props = defineProps<{
  id: string,
  theme?: string,
}>();
const emit = defineEmits(["update:modelValue"]);

const field = ref<any>();
onMounted(() => {
  insertScriptHook(
    'hcaptcha', "https://hcaptcha.com/1/api.js", field,
    true, true,
    (): void => {   /** @ts-ignore **/
      const hcaptcha = window.hcaptcha;
      hcaptcha.render(props.id, {
        sitekey: hcaptcha_sitekey,
        theme: props.theme || "light",
        callback: (val: string): void => (
          emit("update:modelValue", val)
        ),
      });
    }
  )
});

</script>
<template>
  <div ref="field" class="hcaptcha" :id="id" />
</template>

<style scoped>
.hcaptcha {
  margin-top: 2px;
}
</style>