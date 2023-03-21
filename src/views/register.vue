<script setup lang="ts">
import { RouterLink } from "vue-router";
import { reactive, ref } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import HCaptcha from "@/components/captcha/hCaptcha.vue";

const element = ref<FormInstance>();
const form = reactive({
  username: "",
  password: "",
  captcha: "",
});

const rules = reactive<FormRules>({
  username: [
    { required: true, message: 'Please input username', trigger: 'blur' },
    { min: 3, max: 5, message: 'Length should be 3 to 5', trigger: 'blur' },
  ],
  password: [
    {
      required: true,
      message: 'Please input password',
      trigger: 'change',
    },
  ],
  captcha: [
    {
      required: true,
      message: '',
    },
  ],
})

async function submit() {
  await element.value?.validate((valid: boolean, fields) => {
    console.log(valid, fields)
  })
}
</script>

<template>
  <el-container>
    <el-header>
      <RouterLink to="/" class="header">
        <img src="/favicon.ico" alt="Deeptrain">
      </RouterLink>
    </el-header>
    <el-main class="main">
      <h1>Sign up to Deeptrain</h1>
      <el-card shadow="hover">
        <el-form ref="element" :model="form" :rules="rules" :label-position="'top'">
          <el-form-item label="Username or email address" prop="username">
            <el-input v-model="form.username" />
          </el-form-item>
          <el-form-item label="Password" prop="password">
            <el-input v-model="form.password" type="password" show-password />
          </el-form-item>
          <el-form-item prop="captcha">
            <keep-alive>
              <h-captcha id="h-captcha" v-model="form.captcha" />
            </keep-alive>
          </el-form-item>
          <el-button class="validate-button" @click="submit">Sign up</el-button>
        </el-form>
      </el-card>
      <el-card shadow="never" class="help">
        <div>Already have an account? <RouterLink to="/login">Sign in</RouterLink>.</div>
        <div>Forgot password? <RouterLink to="/forgot">Reset password</RouterLink>.</div>
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>
@import "@/assets/css/user.css";
</style>