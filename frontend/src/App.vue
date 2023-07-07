<script setup lang="ts">
import { RouterView } from "vue-router";
import Loader from "@/components/Loader.vue";
import { ready } from "@/assets/script/global";
</script>

<template>
  <router-view v-slot="{ Component }" v-if="ready">
    <transition name="fade">
      <component :is="Component" />
    </transition>
  </router-view>
  <loader v-else />
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  filter: blur(10px);
}

.fade-leave-to {
  display: none;
}
</style>
