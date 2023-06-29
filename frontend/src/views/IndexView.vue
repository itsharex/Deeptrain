<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
</script>
<template>
  <RouterLink to="/register">Register</RouterLink>
  <RouterLink to="/login">Login</RouterLink>
  <RouterLink to="/logout">Logout</RouterLink>
</template>

<style scoped>
@import "@/assets/sytle/index.css";
</style>
