<script setup lang="ts">
import router from "@/router";

const props = defineProps<{
  to: string;
}>();

const path = router.currentRoute;
</script>

<template>
  <router-link
    class="tab"
    :to="props.to"
    :class="{ active: path.path === props.to }"
  >
    <slot />
  </router-link>
</template>

<style>
.tab {
  display: block;
  margin: 4px;
  padding: 8px;
  width: 44px;
  height: 44px;
  background: none;
  border-radius: 4px;
  flex-shrink: 0;
  cursor: pointer;
  transition: 0.25s;
  user-select: none;
  white-space: nowrap;
}

.tab svg {
  width: 28px;
  height: 28px;
  color: rgba(255, 255, 255, 0.6);
  fill: rgba(255, 255, 255, 0.6);
  padding: 2px;
  margin: 0;
}

.tab:hover {
  background: rgba(255, 255, 255, 0.1);
}

.tab.active {
  background: rgb(0, 102, 204);
}

.tab.active svg {
  color: rgba(255, 255, 255, 0.9);
  fill: rgba(255, 255, 255, 0.9);
}
</style>
