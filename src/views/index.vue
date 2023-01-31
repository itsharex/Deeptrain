<script setup>
import { TypingEffect } from '@/assets/js/effect/typing';
import { EarthParticles } from '@/assets/js/effect/earthparticles';

let description = new TypingEffect(
  "We are an Open Source Deep Reinforcement Learning training platform.",
  true,
).run();
document.getElementById("app").appendChild(EarthParticles);
</script>
<template>
  <h1 class="noise">Zh-Website</h1>
  <h3 class="description" v-html="description" />
</template>

<style>
@import "@/assets/css/index.css";
</style>