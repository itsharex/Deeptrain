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
import { useI18n } from "vue-i18n";
import { language } from "@/config";

const { t, locale } = useI18n();
locale.value = language.value;

const element = ref<FormInstance>();
const loading = ref<boolean>(false);
const captcha = ref<Geetest.Geetest | null>(null);
const exp = ref<string>("");
const stamp = ref<number>(0);
const key = ref<string>("");
const form = reactive({
  email: "",
  code: "",
  captcha: {},
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
  code: [
    { required: true, message: t("rule-code"), trigger: "blur" },
    { min: 6, max: 6, message: t("rule-code-format"), trigger: "change" },
  ],
  captcha: [{ required: true, message: "", trigger: "blur" }],
});

async function submit() {
  if (await validateForm(element.value)) {
    loading.value = true;
    try {
      const resp = await axios.post("reset", {
          email: form.email,
          code: form.code,
          key: key.value,
        }),
        data = resp.data;
      if (!data.status)
        ElNotification.error({
          title: t("reset-failed"),
          message: data.reason,
          showClose: false,
        });
      else {
        ElNotification.success({
          title: t("reset-succeeded"),
          message: t("reset-success-message"),
          showClose: false,
        });
        loading.value = false;
        captcha.value?.destroy();
        await router.push("/login");
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

async function post() {
  form.captcha = await getValidateUtilSuccess(captcha.value);
  try {
    const resp = await axios.post("mail/send", form),
      data = resp.data;
    if (!data.status)
      ElNotification.error({
        title: t("reset-failed"),
        message: data.reason,
        showClose: false,
      });
    else {
      key.value = data.key;
      stamp.value = Date.now() / 1000;
      captcha.value?.destroy();
    }
  } catch (e) {
    ElNotification.warning({
      title: t("error-occurred"),
      message: t("network-error"),
      showClose: false,
    });
  }
}

setInterval(() => {
  if (stamp.value + 60 > Date.now() / 1000) {
    exp.value = `(${Math.floor(stamp.value + 60 - Date.now() / 1000)}s)`;
  } else {
    exp.value = "";
  }
}, 500);
</script>

<i18n>
{
  "en": {
    "rule-email": "Please input email",
    "reset-failed": "Reset failed",
    "rule-code": "Please input code",
    "rule-code-format": "Code should be 6 digits",
    "reset-succeeded": "Reset succeeded",
    "reset-success-message": "Your password has been reset. Please check your email for the new password.",
    "error-occurred": "Error occurred",
    "network-error": "There was an error while reset. Please check your network and try again.",
    "reset": "Reset",
    "reset-your-password": "Reset your password",
    "email-address": "Email address",
    "no-account-question": "Do not have an account?",
    "create-one": "Create one",
    "user.email-format-error": "The format of the email is incorrect",
    "user.email-format-unsupported": "Please use a supported email suffix",
    "en-dot": ".",
    "send": "Send",
    "code": "Code"
  },
  "zh": {
    "rule-email": "请输入电子邮箱",
    "rule-code": "请输入验证码",
    "rule-code-format": "验证码应为 6 位数字",
    "reset-failed": "重置失败",
    "reset-succeeded": "重置成功",
    "reset-success-message": "您的密码已重置，请查看您的电子邮箱中查看新密码。",
    "error-occurred": "发生错误",
    "network-error": "重置时发生错误，请检查您的网络并重试。",
    "reset": "重置",
    "reset-your-password": "重置您的密码",
    "email-address": "电子邮箱地址",
    "no-account-question": "没有账号?",
    "create-one": "创建一个",
    "user.email-format-error": "邮箱格式不正确",
    "user.email-format-unsupported": "邮箱后缀不支持，请使用支持的邮箱后缀",
    "en-dot": "",
    "send": "发送",
    "code": "验证码"
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
      <h1>{{ t("reset-your-password") }}</h1>
      <el-card shadow="hover" v-loading="loading">
        <el-form
          ref="element"
          :model="form"
          :rules="rules"
          :label-position="'top'"
        >
          <el-form-item :label="t('email-address')" prop="email">
            <el-input v-model="form.email" type="email" />
          </el-form-item>
          <el-form-item class="inline" :label="t('code')" prop="code">
            <el-input v-model="form.code" :minlength="6" :maxlength="6" />
            <el-button @click="post" :disabled="exp.length > 0">
              {{ t("send") }} {{ exp }}
            </el-button>
          </el-form-item>
          <el-form-item prop="captcha">
            <gee-test id="reset-captcha" v-model="captcha" />
          </el-form-item>
          <el-button class="validate-button" @click="submit">
            {{ t("reset") }}
          </el-button>
        </el-form>
      </el-card>
      <el-card shadow="never" class="help">
        <div>
          {{ t("no-account-question") }}
          <RouterLink to="/register">{{ t("create-one") }}</RouterLink
          >{{ t("en-dot") }}
        </div>
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>
@import "@/assets/style/user.css";
</style>
