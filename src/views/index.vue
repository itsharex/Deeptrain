<script setup>
import { onMounted, ref } from "vue";
import { RouterLink } from 'vue-router';
import { renderer } from '@/assets/js/effect/earthparticles';
import { TypingEffect } from '@/assets/js/effect/typing';
import '@/assets/css/index.css';

let description = new TypingEffect(
  "We are an Open Source Deep Reinforcement Learning training platform.",
  800,
  true,
).run();

const earth = ref();
onMounted(() => {
  renderer(earth.value)
})
</script>
<template>
  <canvas ref="earth" class="earth"></canvas>
  <h1 class="noise">Zh-Website</h1>
  <h3 class="description" v-html="description" />
  <div class="operation-buttons">
    <RouterLink to="/login"><el-button plain>Sign in</el-button></RouterLink>
    <RouterLink to="/register"><el-button>Sign Up</el-button></RouterLink>
  </div>
</template>
