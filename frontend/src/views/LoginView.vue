<script setup lang="ts">
import type { FormInstance, FormRules } from "element-plus";
import { RouterLink } from "vue-router";
import { reactive, ref } from "vue";
import axios from "axios";
import Github from "@/components/icons/github.vue";
import Gitee from "@/components/icons/gitee.vue";
import OLink from "@/components/oauth/olink.vue";
import { validateForm } from "@/assets/script/utils";
import { token } from "@/assets/script/user";
import { refreshState } from "@/assets/script/global";
import router from "@/router";
import { app } from "@/assets/script/allauth";
import GeeTest from "@/components/captcha/GeeTest.vue";
import { getValidateUtilSuccess } from "@/assets/script/captcha/geetest";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const element = ref<FormInstance>();
const loading = ref<boolean>(false);
const captcha = ref<Geetest.Geetest | null>(null);
const form = reactive({
  username: "",
  password: "",
  captcha: {},
});

const rules = reactive<FormRules>({
  username: [
    { required: true, message: t("rule-username"), trigger: "blur" },
    { min: 3, max: 24, message: t("rule-username-length"), trigger: "change" },
  ],
  password: [
    { required: true, message: t("rule-password"), trigger: "blur" },
    { min: 6, max: 46, message: t("rule-password-length"), trigger: "change" },
  ],
  captcha: [{ required: true, message: "", trigger: "blur" }],
});

async function submit() {
  if (await validateForm(element.value)) {
    form.captcha = await getValidateUtilSuccess(captcha.value);
    loading.value = true;
    try {
      const resp = await axios.post("login", form),
        data = resp.data;
      if (!data.status)
        ElNotification.error({
          title: t("login-failed"),
          message: data.reason,
          showClose: false,
        });
      else {
        token.value = data.token;
        ElNotification.success({
          title: t("login-succeeded"),
          message: t("login-success-message", { username: form.username }),
          showClose: false,
        });
        captcha.value?.destroy();
        refreshState({
          callback: (value: number) => {
            app.exec();
            if (value === 2) router.push("/home");
          },
        });
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

app.set();
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
    "no-account-question": "Don't have an account?",
    "sign-in": "Sign in",
    "sign-in-link": "Sign in",
    "username": "Username",
    "password": "Password",
    "forgot-password-question": "Forgot password?",
    "reset-password": "Reset password",
    "create-one": "Create one",
    "sign-in-to-deeptrain": "Sign in to Deeptrain",
    "user.rule-password-not-different": "The new password cannot be the same as the old password",
    "user.rule-password-not-same": "The password does not match",
    "user.email-format-error": "The format of the email is incorrect",
    "user.email-format-unsupported": "Please use a supported email suffix",
    "login-failed": "Login failed",
    "login-succeeded": "Login succeeded",
    "login-success-message": "Welcome back {username}!",
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
    "sign-up-to-deeptrain": "注册 Deeptrain",
    "email-address": "电子邮箱地址",
    "no-account-question": "没有账号?",
    "sign-in": "登录",
    "sign-in-link": "登录",
    "username": "用户名",
    "password": "密码",
    "forgot-password-question": "忘记密码?",
    "reset-password": "重置密码",
    "create-one": "创建一个",
    "sign-in-to-deeptrain": "登录 Deeptrain",
    "user.rule-password-not-different": "新密码不能与原密码相同",
    "user.rule-password-not-same": "两次输入的密码不一致",
    "user.email-format-error": "邮箱格式不正确",
    "user.email-format-unsupported": "邮箱后缀不支持，请使用支持的邮箱后缀",
    "login-failed": "登录失败",
    "login-succeeded": "登录成功",
    "login-success-message": "欢迎回来，{username}！",
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
      <h1>{{ t("sign-in-to-deeptrain") }}</h1>
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
              :minlength="3"
              :maxlength="24"
            />
          </el-form-item>
          <el-form-item :label="t('password')" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              show-password
              :minlength="6"
              :maxlength="46"
            />
          </el-form-item>
          <el-form-item prop="captcha">
            <gee-test id="register-captcha" v-model="captcha" />
          </el-form-item>
          <el-button class="validate-button" @click="submit">{{ t('sign-in') }}</el-button>
        </el-form>
        <el-divider />
        <div class="oauth">
          <o-link uri="https://github.com/"><github /></o-link>
          <o-link uri="https://gitee.com/"><gitee /></o-link>
        </div>
      </el-card>
      <el-card shadow="never" class="help">
        <div>
          {{ t('no-account-question') }}
          <RouterLink to="/register">{{ t('create-one') }}</RouterLink>{{ t('en-dot') }}
        </div>
        <div>
          {{ t('forgot-password-question') }}
          <RouterLink to="/forgot">{{ t('reset-password') }}</RouterLink>{{ t('en-dot') }}
        </div>
      </el-card>
    </el-main>
  </el-container>
</template>


<style scoped>
@import "@/assets/style/user.css";
</style>
