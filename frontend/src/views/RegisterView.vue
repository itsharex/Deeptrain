<script setup lang="ts">
import { RouterLink } from "vue-router";
import { reactive, ref } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import ReCaptcha from "@/components/ReCaptcha.vue";
import { captchaSize, validateEmail, validateRePassword } from "@/assets/script/user";
import axios from "axios";
import { validateForm } from "@/assets/script/utils";

const element = ref<FormInstance>();
const loading = ref<boolean>(false);
const error = ref<string>("");
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
    { min: 3, max: 24, message: 'Length should be 3 to 24', trigger: 'change' },
  ],
  email: [
    { type: 'email', required: true, message: 'Please input email', trigger: 'blur' },
    { validator: validateEmail, trigger: 'change'},
  ],
  password: [
    { required: true, message: 'Please input password', trigger: 'blur' },
    { min: 6, max: 46, message: 'Length should be 6 to 46', trigger: 'change' },
  ],
  repassword: [
    { required: true, message: 'Please input password', trigger: 'blur' },
    { min: 6, max: 46, message: 'Length should be 6 to 46', trigger: 'change' },
    { validator: validateRePassword(form), trigger: 'change' },
  ],
  captcha: [
    { required: true, message: '', trigger: 'blur' },
  ],
})

async function submit() {
  if (await validateForm(element.value)) {
    loading.value = true;
    try {
      const resp = await axios.post('register', form), data = resp.data;
      if (!data.status) ElNotification.error({
          title: "Register failed",
          message: data.reason,
          showClose: false,
        });
      else {
        ElNotification.success({
          title: "Register succeeded",
          message: `Welcome to Deeptrain, ${form.username} !`,
          showClose: false,
        });
      }
    } catch (e) {
      ElNotification.warning({
        title: "Error occurred",
        message: "There was an error while registering. Please check you network and try again.",
        showClose: false,
      });
    }
    loading.value = false;
  }
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
        <el-alert v-if="error" style="transform: translateY(-8px)" :closable="false" :title="error" type="error" show-icon />
        <el-form ref="element" :model="form" :rules="rules" :label-position="'top'">
          <el-form-item label="Username" prop="username">
            <el-input v-model="form.username" type="text" minlength="3" maxlength="24" />
          </el-form-item>
          <el-form-item label="Email address" prop="email">
            <el-input v-model="form.email" type="email" />
          </el-form-item>
          <el-alert type="info" show-icon :closable="false" style="margin-bottom: 4px">
            <p>
              Supported Email Suffixes: <br>
              &nbsp;&nbsp;@gmail.com, @qq.com, <br>
              &nbsp;&nbsp;@outlook.com, @163.com.
            </p>
          </el-alert>
          <el-form-item label="Password" prop="password">
            <el-input v-model="form.password" type="password" show-password minlength="6" maxlength="46" />
          </el-form-item>
          <el-form-item label="Enter the password again" prop="repassword">
            <el-input v-model="form.repassword" type="password" show-password minlength="6" maxlength="46" />
          </el-form-item>
          <el-form-item prop="captcha">
            <re-captcha :size="captchaSize" id="register-captcha" v-model="form.captcha" />
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
@import "@/assets/sytle/user.css";
</style>
