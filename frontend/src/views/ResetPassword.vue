<script setup lang="ts">
import { RouterLink } from "vue-router";
import { reactive, ref } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import { validateEmail } from "@/assets/script/user";
import axios from "axios";
import { validateForm } from "@/assets/script/utils";
import router from "@/router";
import GeeTest from "@/components/captcha/GeeTest.vue";
import { getValidateUtilSuccess } from "@/assets/script/captcha/geetest";

const element = ref<FormInstance>();
const loading = ref<boolean>(false);
const captcha = ref<Geetest.Geetest | null>(null);
const form = reactive({
  username: "",
  email: "",
  password: "",
  repassword: "",
  captcha: {},
});
const rules = reactive<FormRules>({
  email: [
    { type: 'email', required: true, message: 'Please input email', trigger: 'blur' },
    { validator: validateEmail, trigger: 'change'},
  ],
  captcha: [
    { required: true, message: '', trigger: 'blur' },
  ],
})

async function submit() {
  if (await validateForm(element.value)) {
    form.captcha = await getValidateUtilSuccess(captcha.value);
    loading.value = true;
    try {
      const resp = await axios.post('reset', form), data = resp.data;
      if (!data.status) ElNotification.error({
        title: "Reset failed",
        message: data.reason,
        showClose: false,
      });
      else {
        ElNotification.success({
          title: "Reset succeeded",
          message: `Your password has been reset. Please check your email for further instructions.`,
          showClose: false,
        });
        loading.value = false;
        captcha.value?.destroy();
        await router.push('/login');
      }
    } catch (e) {
      ElNotification.warning({
        title: "Error occurred",
        message: "There was an error while reset. Please check you network and try again.",
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
      <h1>Reset your password</h1>
      <el-card shadow="hover" v-loading="loading">
        <el-form ref="element" :model="form" :rules="rules" :label-position="'top'">
          <el-form-item label="Email address" prop="email">
            <el-input v-model="form.email" type="email" />
          </el-form-item>
          <el-form-item prop="captcha">
            <gee-test id="reset-captcha" v-model="captcha" />
          </el-form-item>
          <el-button class="validate-button" @click="submit">Reset</el-button>
        </el-form>
      </el-card>
      <el-card shadow="never" class="help">
        <div>Do not have an account? <RouterLink to="/register">Create one</RouterLink>.</div>
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>
@import "@/assets/sytle/user.css";
</style>
