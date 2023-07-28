<script setup lang="ts">
import { RouterLink } from "vue-router";
import { reactive, ref } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import { token, validateEmail, validateRePassword } from "@/assets/script/user";
import axios from "axios";
import { state } from "@/assets/script/global";
import { validateForm } from "@/assets/script/utils";
import router from "@/router";
import GeeTest from "@/components/captcha/GeeTest.vue";
import { getValidateUtilSuccess } from "@/assets/script/captcha/geetest";
import { useI18n } from "vue-i18n";
import { language } from "@/config";

const { t, locale } = useI18n();
locale.value = language.value;

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
  username: [
    { required: true, message: t("rule-username"), trigger: "blur" },
    { min: 3, max: 24, message: t("rule-username-length"), trigger: "change" },
  ],
  email: [
    {
      type: "email",
      required: true,
      message: t("rule-email"),
      trigger: "blur",
    },
    { validator: validateEmail(t), trigger: "change" },
  ],
  password: [
    { required: true, message: t("rule-password"), trigger: "blur" },
    { min: 6, max: 46, message: t("rule-password-length"), trigger: "change" },
  ],
  repassword: [
    { required: true, message: t("rule-re-password"), trigger: "blur" },
    { min: 6, max: 46, message: t("rule-password-length"), trigger: "change" },
    { validator: validateRePassword(t, form), trigger: "change" },
  ],
  captcha: [{ required: true, message: "", trigger: "blur" }],
});

async function submit() {
  if (await validateForm(element.value)) {
    form.captcha = await getValidateUtilSuccess(captcha.value);
    loading.value = true;
    try {
      const resp = await axios.post("register", form),
        data = resp.data;
      if (!data.status)
        ElNotification.error({
          title: t("register-failed"),
          message: data.reason,
          showClose: false,
        });
      else {
        token.value = data.token;
        ElNotification.success({
          title: t("register-succeeded"),
          message: t("register-success-message", { username: form.username }),
          showClose: false,
        });
        loading.value = false;
        captcha.value?.destroy();
        state.value = 1;
        await router.push("/verify");
      }
    } catch (e) {
      ElNotification.warning({
        title: t("error-occurred"),
        message: t("network-error"),
        showClose: false,
      });
    }
    loading.value = false;
  }
}
</script>

<i18n>
{
  "en": {
    "rule-username": "Please input username",
    "rule-username-length": "Length should be 3 to 24",
    "rule-email": "Please input email",
    "rule-password": "Please input password",
    "rule-re-password": "Please input password",
    "rule-password-length": "Length should be 6 to 46",
    "register-failed": "Register failed",
    "register-succeeded": "Register succeeded",
    "register-success-message": "Welcome to Deeptrain, {username}!",
    "error-occurred": "Error occurred",
    "network-error": "There was an error while registering. Please check your network and try again.",
    "sign-up": "Sign up",
    "sign-up-to-deeptrain": "Sign up to Deeptrain",
    "email-address": "Email address",
    "no-account-question": "Already have an account?",
    "sign-in": "Sign in",
    "sign-in-link": "Sign in",
    "enter-password-again": "Enter password again",
    "username": "Username",
    "password": "Password",
    "supported-email-suffixes": "Supported Email Suffixes",
    "user.rule-password-not-different": "The new password cannot be the same as the old password",
    "user.rule-password-not-same": "The password does not match",
    "user.email-format-error": "The format of the email is incorrect",
    "user.email-format-unsupported": "Please use a supported email suffix",
    "en-dot": "."
  },
  "zh": {
    "rule-username": "请输入用户名",
    "rule-username-length": "长度应为 3 到 24",
    "rule-email": "请输入电子邮箱",
    "rule-password": "请输入密码",
    "rule-re-password": "请输入密码",
    "rule-password-length": "长度应为 6 到 46",
    "register-failed": "注册失败",
    "register-succeeded": "注册成功",
    "register-success-message": "欢迎加入 Deeptrain，{username}！",
    "error-occurred": "发生错误",
    "network-error": "注册时发生错误，请检查您的网络并重试。",
    "sign-up": "注册",
    "sign-up-to-deeptrain": "Deeptrain 注册",
    "email-address": "电子邮箱地址",
    "no-account-question": "已有账号?",
    "sign-in": "登录",
    "sign-in-link": "登录",
    "enter-password-again": "再次输入密码",
    "username": "用户名",
    "password": "密码",
    "supported-email-suffixes": "支持的邮箱后缀",
    "user.rule-password-not-different": "新密码不能与原密码相同",
    "user.rule-password-not-same": "两次输入的密码不一致",
    "user.email-format-error": "邮箱格式不正确",
    "user.email-format-unsupported": "邮箱后缀不支持，请使用支持的邮箱后缀",
    "en-dot": ""
  }
}
</i18n>

<template>
  <el-container>
    <el-header>
      <RouterLink to="/" class="header">
        <img src="/favicon.ico" alt="Deeptrain" />
      </RouterLink>
    </el-header>
    <el-main class="main">
      <h1>{{ t("sign-up-to-deeptrain") }}</h1>
      <el-card shadow="hover" v-loading="loading">
        <el-form
          ref="element"
          :model="form"
          :rules="rules"
          :label-position="'top'"
        >
          <el-form-item :label="t('username')" prop="username">
            <el-input
              v-model="form.username"
              type="text"
              minlength="3"
              maxlength="24"
            />
          </el-form-item>
          <el-form-item :label="t('email-address')" prop="email">
            <el-input v-model="form.email" type="email" />
          </el-form-item>
          <el-alert
            type="info"
            show-icon
            :closable="false"
            style="margin-bottom: 4px"
          >
            <p>
              {{ t("supported-email-suffixes") }}:<br />&nbsp;&nbsp;@gmail.com,
              @qq.com, <br />&nbsp;&nbsp;@outlook.com, @163.com.
            </p>
          </el-alert>
          <el-form-item :label="t('password')" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              show-password
              minlength="6"
              maxlength="46"
            />
          </el-form-item>
          <el-form-item :label="t('enter-password-again')" prop="repassword">
            <el-input
              v-model="form.repassword"
              type="password"
              show-password
              minlength="6"
              maxlength="46"
            />
          </el-form-item>
          <el-form-item prop="captcha">
            <gee-test id="register-captcha" v-model="captcha" />
          </el-form-item>
          <el-button class="validate-button" @click="submit">
            {{ t("sign-up") }}
          </el-button>
        </el-form>
      </el-card>
      <el-card shadow="never" class="help">
        <div>
          {{ t("no-account-question") }}
          <RouterLink to="/login">{{ t("sign-in-link") }}</RouterLink
          >{{ t("en-dot") }}
        </div>
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>
@import "@/assets/style/user.css";
</style>
