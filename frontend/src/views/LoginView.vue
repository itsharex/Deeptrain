<script setup lang="ts">
import type { FormInstance, FormRules } from "element-plus";
import { RouterLink } from "vue-router";
import { reactive, ref } from "vue";
import axios from "axios";
import { performCheck } from "@/assets/script/invisible";
import Github from "@/components/icons/github.vue";
import Gitee from "@/components/icons/gitee.vue";
import OLink from "@/components/oauth/olink.vue";
import { validateForm } from "@/assets/script/utils";
import { token } from "@/assets/script/user";

const element = ref<FormInstance>();
const loading = ref<boolean>(false);
const error = ref<string>("");
const form = reactive({
  username: "",
  password: "",
  captcha: "",
});

const rules = reactive<FormRules>({
  username: [
    { required: true, message: 'Please input username', trigger: 'blur' },
    { min: 3, max: 24, message: 'Length should be 3 to 24', trigger: 'change' },
  ],
  password: [
    { required: true, message: 'Please input password', trigger: 'blur' },
    { min: 6, max: 46, message: 'Length should be 6 to 46', trigger: 'change' },
  ],
  captcha: [
    { required: true, message: '', trigger: 'blur' },
  ],
})

async function submit(e: Event) {
  form.captcha = await performCheck(e);
  if (await validateForm(element.value)) {
    loading.value = true;
    try {
      const resp = await axios.post('login', form), data = resp.data;
      if (!data.status) ElNotification.error({
          title: "Login failed",
          message: data.reason,
          showClose: false,
        });
      else {
        token.value = data.token;
        ElNotification.success({
          title: "Login succeeded",
          message: `Welcome back ${form.username} !`,
          showClose: false,
        });
      }
    } catch (e) {
      ElNotification.warning({
        title: "Error occurred",
        message: "There was an error while logging in. Please check you network and try again.",
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
      <h1>Sign in to Deeptrain</h1>
      <el-card shadow="hover" v-loading="loading">
        <el-alert v-if="error" style="transform: translateY(-8px)" :closable="false" :title="error" type="error" show-icon />
        <el-form ref="element" :model="form" :rules="rules" :label-position="'top'">
          <el-form-item label="Username" prop="username">
            <el-input v-model="form.username" type="text" minlength="3" maxlength="24" />
          </el-form-item>
          <el-form-item label="Password" prop="password">
            <el-input v-model="form.password" type="password" show-password minlength="6" maxlength="46" />
          </el-form-item><br>
          <el-button class="validate-button" @click="submit">Sign in</el-button>
        </el-form>
        <el-divider />
        <div class="oauth">
          <o-link uri="https://github.com/"><github /></o-link>
          <o-link uri="https://gitee.com/"><gitee /></o-link>
        </div>
      </el-card>
      <el-card shadow="never" class="help">
        <div>Do not have an account? <RouterLink to="/register">Create one</RouterLink>.</div>
        <div>Forgot password? <RouterLink to="/forgot">Reset password</RouterLink>.</div>
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>
@import "@/assets/sytle/user.css";
</style>
