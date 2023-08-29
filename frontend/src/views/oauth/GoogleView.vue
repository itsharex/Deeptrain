<script setup lang="ts">
import axios from "axios";
import { useI18n } from "vue-i18n";
import { language, oauth } from "@/config";
import { reactive, ref } from "vue";
import { RouterLink } from "vue-router";
import type { FormInstance, FormRules } from "element-plus";
import { token, validateEmail } from "@/assets/script/user";
import { refreshState, state } from "@/assets/script/global";
import { app } from "@/assets/script/allauth";
import router from "@/router";
import { validateForm } from "@/assets/script/utils";
import BoxLoader from "@/components/BoxLoader.vue";

const { t, locale } = useI18n();
locale.value = language.value;

const element = ref<FormInstance>();
const param = new URLSearchParams(window.location.search);
const code = param.get("code");
const preflight = ref(false);
const form = reactive({
  username: "",
  email: "",
});

const rules = reactive<FormRules>({
  email: [
    {
      type: "email",
      required: true,
      message: t("rule-email"),
      trigger: "blur",
    },
    { validator: validateEmail(t), trigger: "change" },
  ],
});

if (state.value !== 2)
  axios
    .get("oauth/google/preflight?code=" + code)
    .then((res) => {
      if (!res.data.status) {
        ElMessage({
          message: res.data.error,
          type: "error",
        });
        setTimeout(() => router.push("/login"), 500);
        return;
      }

      if (res.data.register) {
        form.username = res.data.username;
        form.email = res.data.email;
        preflight.value = true;
      } else {
        ElNotification.success({
          title: t("login-succeeded"),
          message: t("login-success-message", { username: res.data.username }),
          showClose: false,
        });

        token.value = res.data.token;
        axios.defaults.headers.common["Authorization"] = token.value;
        refreshState({
          callback: (value: number) => {
            app.exec();
            if (value === 2) router.push("/home");
          },
        });
      }
    })
    .catch((err) => {
      ElMessage({
        message: t("network-error"),
        type: "error",
      });
      console.debug(err);
    });
else
  axios
    .get("oauth/google/connect?code=" + code)
    .then((res) => {
      if (!res.data.status) {
        ElMessage({
          message: res.data.error,
          type: "error",
        });
        setTimeout(() => router.push("/home"), 500);
        return;
      }

      ElNotification.success({
        title: t("bind-succeeded"),
        message: t("bind-success-message"),
        showClose: false,
      });

      setTimeout(() => router.push("/home"), 500);
    })
    .catch((err) => {
      ElMessage({
        message: t("network-error"),
        type: "error",
      });
      console.debug(err);
    });

async function register() {
  if (await validateForm(element.value)) {
    axios
      .post("oauth/google/register", {
        code: code,
        username: form.username,
        email: form.email,
      })
      .then((res) => {
        if (!res.data.status) {
          ElMessage({
            message: res.data.error,
            type: "error",
          });
          return;
        }

        token.value = res.data.token;
        axios.defaults.headers.common["Authorization"] = token.value;
        refreshState({
          callback: (value: number) => {
            app.exec();
            if (value === 1) router.push("/verify");
            if (value === 2) router.push("/home");
          },
        });
      })
      .catch((err) => {
        ElMessage({
          message: t("network-error"),
          type: "error",
        });
        console.debug(err);
      });
  }
}
</script>
<i18n>
{
  "en": {
    "network-error": "There is something wrong with the network.",
    "sign-up-to-deeptrain": "Sign up to Deeptrain",
    "continue": "Continue as {username}",
    "sign-up": "Sign up",
    "email-address": "Email",
    "rule-email": "Please input email",
    "register-succeeded": "Register succeeded",
    "register-success-message": "Welcome to Deeptrain, {username}!",
    "login-succeeded": "Login succeeded",
    "login-success-message": "Welcome back, {username}!",
    "bind-succeeded": "Bind succeeded",
    "bind-success-message": "Successfully binded acoount!",
    "user.email-format-error": "The format of the email is incorrect",
    "user.email-format-unsupported": "Please use a supported email suffix"
  },
  "zh": {
    "network-error": "网络连接错误！请检查您的网络连接",
    "sign-up-to-deeptrain": "注册 Deeptrain",
    "continue": "以 {username} 继续",
    "sign-up": "注册",
    "email-address": "邮箱",
    "rule-email": "请输入邮箱",
    "register-succeeded": "注册成功",
    "register-success-message": "欢迎来到 Deeptrain，{username}！",
    "login-succeeded": "登录成功",
    "login-success-message": "欢迎回来，{username}！",
    "bind-succeeded": "绑定成功",
    "bind-success-message": "成功绑定账号！",
    "user.email-format-error": "邮箱格式不正确",
    "user.email-format-unsupported": "邮箱后缀不支持，请使用支持的邮箱后缀"
  }
}
</i18n>
<template>
  <div class="register" v-if="preflight">
    <el-container>
      <el-header>
        <RouterLink to="/" class="header">
          <img src="/favicon.ico" alt="Deeptrain" />
        </RouterLink>
      </el-header>
      <el-main class="main">
        <h1>{{ t("sign-up-to-deeptrain") }}</h1>
        <el-card shadow="hover">
          <div class="tips">
            {{ t("continue", { username: form.username }) }}
          </div>
          <br />
          <el-form
            :model="form"
            :rules="rules"
            ref="element"
            label-position="left"
          >
            <el-form-item :label="t('email-address')" prop="email">
              <el-input
                v-model="form.email"
                minlength="6"
                maxlength="46"
                type="email"
              />
            </el-form-item>
            <div style="height: 6px" />
            <el-button class="validate-button" @click="register">{{
              t("sign-up")
            }}</el-button>
          </el-form>
        </el-card>
      </el-main>
    </el-container>
  </div>
  <BoxLoader v-else />
</template>

<style scoped>
@import "@/assets/style/user.css";

.tips {
  text-align: center;
  user-select: none;
}
</style>
