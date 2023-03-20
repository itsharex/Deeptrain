<script setup lang="ts">
import Turnstile from "@/components/captcha/Turnstile.vue";
import { RouterLink } from "vue-router";
import { ref } from "vue";

const form = ref({
  username: "",
  password: "",
  captcha: "",
})
</script>

<template>
  <el-container>
    <el-header>
      <RouterLink to="/" class="header">
        <img src="/favicon.ico" alt="Deeptrain">
      </RouterLink>
    </el-header>
    <el-main class="main">
      <h1>Sign in to Deeptrain</h1>
      <el-card shadow="hover">
        <el-form :model="form" :label-position="'top'">
          <el-form-item label="Username or email address">
            <el-input v-model="form.username" />
          </el-form-item>
          <el-form-item label="Password">
            <el-input v-model="form.password" type="password" show-password />
          </el-form-item>
          <Turnstile id="cf-captcha" v-model="form.captcha" />
          <el-button class="validate-button">Sign in</el-button>
        </el-form>
        <el-divider />
        <p class="oauth-tag">Sign in with OAuth</p>
        <p>{{ form }}</p>
      </el-card>
      <el-card shadow="never" class="help">
        Do not have an account? <RouterLink to="/register">Create one</RouterLink>.
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>
.header {
  margin: 20px auto;
  display: flex;
  width: max-content;
  background: none !important;
}
.header img {
  width: 64px;
  height: 64px;
}
.main {
  margin: 20px 0;
  display: grid;
  grid-gap: 24px;
  justify-content: center;
}
.main h1 {
  color: #fff;
  font-weight: 100;
  text-align: center;
  height: max-content;
}
#cf-captcha {
  margin: 10px 0;
  border-radius: 2px;
}
.oauth-tag {
  text-align: center;
  transform: translateY(-16px);
}
.validate-button {
  background: #238623;
  color: #fff !important;
  border-color: rgba(240, 246, 252, 0.1) !important;
  width: 100%;
}
.validate-button:hover,
.validate-button:active,
.validate-button:focus {
  background: #2ea043;
}
.help {
  padding: 8px 20px;
  background: transparent;
  text-align: center;
}
</style>