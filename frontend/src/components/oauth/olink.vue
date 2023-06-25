<script setup lang="ts">
import { redirect } from "@/assets/script/utils";

const props = defineProps<{
  uri: string,
}>();

function click() {
  redirect(props.uri);
}
</script>

<template>
  <a @click="click" class="oauth-link">
    <slot />
  </a>
</template>
