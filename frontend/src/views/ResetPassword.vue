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

const { t } = useI18n();

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
    {
      type: "email",
      required: true,
      message: t("rule-email"),
      trigger: "blur",
    },
    { validator: validateEmail(t), trigger: "change" },
  ],
  captcha: [{ required: true, message: "", trigger: "blur" }],
});

async function submit() {
  if (await validateForm(element.value)) {
    form.captcha = await getValidateUtilSuccess(captcha.value);
    loading.value = true;
    try {
      const resp = await axios.post("reset", form),
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
</script>

<i18n>
{
  "en": {
    "rule-email": "Please input email",
    "reset-failed": "Reset failed",
    "reset-succeeded": "Reset succeeded",
    "reset-success-message": "Your password has been reset. Please check your email for further instructions.",
    "error-occurred": "Error occurred",
    "network-error": "There was an error while reset. Please check your network and try again.",
    "user.email-format-error": "The format of the email is incorrect",
    "user.email-format-unsupported": "Please use a supported email suffix"
  },
  "zh": {
    "rule-email": "请输入电子邮箱",
    "reset-failed": "重置失败",
    "reset-succeeded": "重置成功",
    "reset-success-message": "您的密码已重置，请查看您的电子邮箱获取进一步说明。",
    "error-occurred": "发生错误",
    "network-error": "重置时发生错误，请检查您的网络并重试。",
    "user.email-format-error": "邮箱格式不正确",
    "user.email-format-unsupported": "邮箱后缀不支持，请使用支持的邮箱后缀"
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
      <h1>Reset your password</h1>
      <el-card shadow="hover" v-loading="loading">
        <el-form
          ref="element"
          :model="form"
          :rules="rules"
          :label-position="'top'"
        >
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
        <div>
          Do not have an account?
          <RouterLink to="/register">Create one</RouterLink>.
        </div>
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>
@import "@/assets/style/user.css";
</style>
