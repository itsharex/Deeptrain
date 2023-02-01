<script setup lang="ts">
import HCaptcha from "@/components/captcha/hCaptcha.vue";
import Turnstile from "@/components/captcha/Turnstile.vue";
import { ref } from "vue";
import type { Ref } from "vue";

const datakey: Ref<string> = ref("");
const datakey2: Ref<string> = ref("");
const datakey3: Ref<string> = ref("");
const datakey4: Ref<string> = ref("");
</script>

<template>
  <p>1 {{ datakey }} </p><hCaptcha id="hcaptcha-field" v-model="datakey" />
  <p>2 {{ datakey2 }} </p><hCaptcha id="hcaptcha-field2" theme="dark" v-model="datakey2" />
  <p>3 {{ datakey3 }} </p><Turnstile id="hcaptcha-field3" theme="light" v-model="datakey3" />
  <p>4 {{ datakey4 }} </p><Turnstile id="hcaptcha-field4" v-model="datakey4" />
</template>

<style scoped>

</style>