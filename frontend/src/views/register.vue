<script setup lang="ts">
import { RouterLink } from "vue-router";
import { reactive, ref } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import HCaptcha from "@/components/captcha/hCaptcha.vue";
import { validateEmail, validateRePassword } from "@/assets/js/utils";

const element = ref<FormInstance>();
const loading = ref<boolean>(false);
const form = reactive({
  username: "",
  email: "",
  password: "",
  repassword: "",
  captcha: "",
});

const rules = reactive<FormRules>({
  username: [
    { required: true, message: 'Please input username', trigger: 'blur' },
    { min: 3, max: 14, message: 'Length should be 3 to 14', trigger: 'change' },
  ],
  email: [
    { type: 'email', required: true, message: 'Please input email', trigger: 'blur' },
    { validator: validateEmail, trigger: 'change'},
  ],
  password: [
    { required: true, message: 'Please input password', trigger: 'blur' },
    { min: 6, max: 26, message: 'Length should be 6 to 26', trigger: 'change' },
  ],
  repassword: [
    { required: true, message: 'Please input password', trigger: 'blur' },
    { min: 6, max: 26, message: 'Length should be 6 to 26', trigger: 'change' },
    { validator: validateRePassword(form), trigger: 'change' },
  ],
  captcha: [
    { required: true, message: '', trigger: 'blur' },
  ],
})

async function submit() {
  await element.value?.validate((valid: boolean, fields) => {
    if (valid) {
      loading.value = true;
    }
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
      <el-card shadow="hover" v-loading="loading">
        <el-form ref="element" :model="form" :rules="rules" :label-position="'top'">
          <el-form-item label="Username" prop="username">
            <el-input v-model="form.username" type="text" minlength="3" maxlength="14" />
          </el-form-item>
          <el-form-item label="Email address" prop="email">
            <el-input v-model="form.email" type="email" />
          </el-form-item>
          <el-alert type="info" show-icon :closable="false">
            <p>
              Supported Email Suffixes: <br>
              &nbsp;&nbsp;@gmail.com, @qq.com, <br>
              &nbsp;&nbsp;@yahoo.com, @163.com, <br>
              &nbsp;&nbsp;@dingtalk.com.
            </p>
          </el-alert>
          <el-form-item label="Password" prop="password">
            <el-input v-model="form.password" type="password" show-password minlength="6" maxlength="26" />
          </el-form-item>
          <el-form-item label="Enter the password again" prop="repassword">
            <el-input v-model="form.repassword" type="password" show-password minlength="6" maxlength="26" />
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
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>
@import "@/assets/css/user.css";
</style>