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
    .get("oauth/github/preflight?code=" + code)
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
    .get("oauth/github/connect?code=" + code)
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
      .post("oauth/github/register", {
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
  <div class="banter-loader" v-else>
    <div class="banter-loader__box" />
    <div class="banter-loader__box" />
    <div class="banter-loader__box" />
    <div class="banter-loader__box" />
    <div class="banter-loader__box" />
    <div class="banter-loader__box" />
    <div class="banter-loader__box" />
    <div class="banter-loader__box" />
    <div class="banter-loader__box" />
  </div>
</template>

<style scoped>
@import "@/assets/style/user.css";

.tips {
  text-align: center;
  user-select: none;
}

.banter-loader {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 72px;
  height: 72px;
  margin-left: -36px;
  margin-top: -36px;
}

.banter-loader__box {
  float: left;
  position: relative;
  width: 20px;
  height: 20px;
  margin-right: 6px;
}

.banter-loader__box:before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: #fff;
}

.banter-loader__box:nth-child(3n) {
  margin-right: 0;
  margin-bottom: 6px;
}

.banter-loader__box:nth-child(1):before,
.banter-loader__box:nth-child(4):before {
  margin-left: 26px;
}

.banter-loader__box:nth-child(3):before {
  margin-top: 52px;
}

.banter-loader__box:last-child {
  margin-bottom: 0;
}

@keyframes moveBox-1 {
  9.0909090909% {
    transform: translate(-26px, 0);
  }

  18.1818181818% {
    transform: translate(0px, 0);
  }

  27.2727272727% {
    transform: translate(0px, 0);
  }

  36.3636363636% {
    transform: translate(26px, 0);
  }

  45.4545454545% {
    transform: translate(26px, 26px);
  }

  54.5454545455% {
    transform: translate(26px, 26px);
  }

  63.6363636364% {
    transform: translate(26px, 26px);
  }

  72.7272727273% {
    transform: translate(26px, 0px);
  }

  81.8181818182% {
    transform: translate(0px, 0px);
  }

  90.9090909091% {
    transform: translate(-26px, 0px);
  }

  100% {
    transform: translate(0px, 0px);
  }
}

.banter-loader__box:nth-child(1) {
  animation: moveBox-1 4s infinite;
}

@keyframes moveBox-2 {
  9.0909090909% {
    transform: translate(0, 0);
  }

  18.1818181818% {
    transform: translate(26px, 0);
  }

  27.2727272727% {
    transform: translate(0px, 0);
  }

  36.3636363636% {
    transform: translate(26px, 0);
  }

  45.4545454545% {
    transform: translate(26px, 26px);
  }

  54.5454545455% {
    transform: translate(26px, 26px);
  }

  63.6363636364% {
    transform: translate(26px, 26px);
  }

  72.7272727273% {
    transform: translate(26px, 26px);
  }

  81.8181818182% {
    transform: translate(0px, 26px);
  }

  90.9090909091% {
    transform: translate(0px, 26px);
  }

  100% {
    transform: translate(0px, 0px);
  }
}

.banter-loader__box:nth-child(2) {
  animation: moveBox-2 4s infinite;
}

@keyframes moveBox-3 {
  9.0909090909% {
    transform: translate(-26px, 0);
  }

  18.1818181818% {
    transform: translate(-26px, 0);
  }

  27.2727272727% {
    transform: translate(0px, 0);
  }

  36.3636363636% {
    transform: translate(-26px, 0);
  }

  45.4545454545% {
    transform: translate(-26px, 0);
  }

  54.5454545455% {
    transform: translate(-26px, 0);
  }

  63.6363636364% {
    transform: translate(-26px, 0);
  }

  72.7272727273% {
    transform: translate(-26px, 0);
  }

  81.8181818182% {
    transform: translate(-26px, -26px);
  }

  90.9090909091% {
    transform: translate(0px, -26px);
  }

  100% {
    transform: translate(0px, 0px);
  }
}

.banter-loader__box:nth-child(3) {
  animation: moveBox-3 4s infinite;
}

@keyframes moveBox-4 {
  9.0909090909% {
    transform: translate(-26px, 0);
  }

  18.1818181818% {
    transform: translate(-26px, 0);
  }

  27.2727272727% {
    transform: translate(-26px, -26px);
  }

  36.3636363636% {
    transform: translate(0px, -26px);
  }

  45.4545454545% {
    transform: translate(0px, 0px);
  }

  54.5454545455% {
    transform: translate(0px, -26px);
  }

  63.6363636364% {
    transform: translate(0px, -26px);
  }

  72.7272727273% {
    transform: translate(0px, -26px);
  }

  81.8181818182% {
    transform: translate(-26px, -26px);
  }

  90.9090909091% {
    transform: translate(-26px, 0px);
  }

  100% {
    transform: translate(0px, 0px);
  }
}

.banter-loader__box:nth-child(4) {
  animation: moveBox-4 4s infinite;
}

@keyframes moveBox-5 {
  9.0909090909% {
    transform: translate(0, 0);
  }

  18.1818181818% {
    transform: translate(0, 0);
  }

  27.2727272727% {
    transform: translate(0, 0);
  }

  36.3636363636% {
    transform: translate(26px, 0);
  }

  45.4545454545% {
    transform: translate(26px, 0);
  }

  54.5454545455% {
    transform: translate(26px, 0);
  }

  63.6363636364% {
    transform: translate(26px, 0);
  }

  72.7272727273% {
    transform: translate(26px, 0);
  }

  81.8181818182% {
    transform: translate(26px, -26px);
  }

  90.9090909091% {
    transform: translate(0px, -26px);
  }

  100% {
    transform: translate(0px, 0px);
  }
}

.banter-loader__box:nth-child(5) {
  animation: moveBox-5 4s infinite;
}

@keyframes moveBox-6 {
  9.0909090909% {
    transform: translate(0, 0);
  }

  18.1818181818% {
    transform: translate(-26px, 0);
  }

  27.2727272727% {
    transform: translate(-26px, 0);
  }

  36.3636363636% {
    transform: translate(0px, 0);
  }

  45.4545454545% {
    transform: translate(0px, 0);
  }

  54.5454545455% {
    transform: translate(0px, 0);
  }

  63.6363636364% {
    transform: translate(0px, 0);
  }

  72.7272727273% {
    transform: translate(0px, 26px);
  }

  81.8181818182% {
    transform: translate(-26px, 26px);
  }

  90.9090909091% {
    transform: translate(-26px, 0px);
  }

  100% {
    transform: translate(0px, 0px);
  }
}

.banter-loader__box:nth-child(6) {
  animation: moveBox-6 4s infinite;
}

@keyframes moveBox-7 {
  9.0909090909% {
    transform: translate(26px, 0);
  }

  18.1818181818% {
    transform: translate(26px, 0);
  }

  27.2727272727% {
    transform: translate(26px, 0);
  }

  36.3636363636% {
    transform: translate(0px, 0);
  }

  45.4545454545% {
    transform: translate(0px, -26px);
  }

  54.5454545455% {
    transform: translate(26px, -26px);
  }

  63.6363636364% {
    transform: translate(0px, -26px);
  }

  72.7272727273% {
    transform: translate(0px, -26px);
  }

  81.8181818182% {
    transform: translate(0px, 0px);
  }

  90.9090909091% {
    transform: translate(26px, 0px);
  }

  100% {
    transform: translate(0px, 0px);
  }
}

.banter-loader__box:nth-child(7) {
  animation: moveBox-7 4s infinite;
}

@keyframes moveBox-8 {
  9.0909090909% {
    transform: translate(0, 0);
  }

  18.1818181818% {
    transform: translate(-26px, 0);
  }

  27.2727272727% {
    transform: translate(-26px, -26px);
  }

  36.3636363636% {
    transform: translate(0px, -26px);
  }

  45.4545454545% {
    transform: translate(0px, -26px);
  }

  54.5454545455% {
    transform: translate(0px, -26px);
  }

  63.6363636364% {
    transform: translate(0px, -26px);
  }

  72.7272727273% {
    transform: translate(0px, -26px);
  }

  81.8181818182% {
    transform: translate(26px, -26px);
  }

  90.9090909091% {
    transform: translate(26px, 0px);
  }

  100% {
    transform: translate(0px, 0px);
  }
}

.banter-loader__box:nth-child(8) {
  animation: moveBox-8 4s infinite;
}

@keyframes moveBox-9 {
  9.0909090909% {
    transform: translate(-26px, 0);
  }

  18.1818181818% {
    transform: translate(-26px, 0);
  }

  27.2727272727% {
    transform: translate(0px, 0);
  }

  36.3636363636% {
    transform: translate(-26px, 0);
  }

  45.4545454545% {
    transform: translate(0px, 0);
  }

  54.5454545455% {
    transform: translate(0px, 0);
  }

  63.6363636364% {
    transform: translate(-26px, 0);
  }

  72.7272727273% {
    transform: translate(-26px, 0);
  }

  81.8181818182% {
    transform: translate(-52px, 0);
  }

  90.9090909091% {
    transform: translate(-26px, 0);
  }

  100% {
    transform: translate(0px, 0);
  }
}

.banter-loader__box:nth-child(9) {
  animation: moveBox-9 4s infinite;
}
</style>
