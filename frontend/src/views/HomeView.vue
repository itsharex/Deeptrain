<script setup lang="ts">
import { ref } from "vue";
import { RouterLink } from "vue-router";
import { state } from "@/assets/script/global";
import Translate from "@/components/icons/translate.vue";
import Home from "@/components/icons/home.vue";
import Login from "@/components/icons/login.vue";
import Setting from "@/components/icons/setting.vue";

const I18nPopover = ref(null);

const currentIcon = ref<HTMLElement | null>(null);
function iconToggle(e: Event) {
  let target = e.target as HTMLElement;
  const name = target.localName;
  if (name === "path") target = target.parentElement as HTMLElement;
  if (name === "a") target = target.children[0] as HTMLElement;
  target.classList.add("checked");
  console.log(currentIcon.value);
  if (currentIcon.value) currentIcon.value.classList.remove("checked");
}
</script>
<template>

</template>

<style scoped>
@import "@/assets/sytle/index.css";
</style>
