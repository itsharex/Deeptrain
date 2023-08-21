<script setup lang="ts">
import type { FormInstance, FormRules } from "element-plus";
import { RouterLink } from "vue-router";
import { reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import axios from "axios";
import { validateForm } from "@/assets/script/utils";
import router from "@/router";
import { state } from "@/assets/script/global";
import { app } from "@/assets/script/allauth";
import { language } from "@/config";

const element = ref<FormInstance>();
const loading = ref<boolean>(false);
const form = reactive({
  code: "",
});
const { t, locale } = useI18n();
locale.value = language.value;

const rules = reactive<FormRules>({
  code: [
    {
      required: true,
      message: t("rule-code"),
      trigger: "blur",
    },
    {
      min: 6,
      max: 6,
      message: t("rule-code-format"),
      trigger: "change",
    },
  ],
});

async function submit() {
  if (await validateForm(element.value)) {
    loading.value = true;
    try {
      const resp = await axios.post("verify", form),
        data = resp.data;
      if (!data.status)
        ElNotification.error({
          title: t("verify-failed"),
          message: data.reason,
          showClose: false,
        });
      else {
        state.value = 2;
        app.exec();
        ElNotification.success({
          title: t("verify-succeeded"),
          message: `Welcome to Deeptrain!`,
          showClose: false,
        });
        await router.push("/home");
      }
    } catch (e) {
      ElNotification.warning({
        title: t("error-occurred"),
        message: t("verify-error"),
        showClose: false,
      });
    }
    loading.value = false;
  }
}

async function resend() {
  loading.value = true;
  try {
    const resp = await axios.post("resend", form),
      data = resp.data;
    if (!data.status)
      ElNotification.error({
        title: t("resend-failed"),
        message: data.reason,
        showClose: false,
      });
    else
      ElNotification.success({
        title: t("resend-succeeded"),
        message: t("tips"),
        showClose: false,
      });
  } catch (e) {
    ElNotification.warning({
      title: t("error-occurred"),
      message: t("resend-error"),
      showClose: false,
    });
  }
  loading.value = false;
}
</script>

<template>
  <el-container>
    <el-header>
      <RouterLink to="/" class="header">
        <img src="/favicon.ico" alt="Deeptrain" />
      </RouterLink>
    </el-header>
    <el-main class="main">
      <h1>{{ t("verify") }}</h1>
      <el-card shadow="hover" v-loading="loading">
        <div class="tips">{{ t("tips") }}</div>
        <el-form
          ref="element"
          :model="form"
          :rules="rules"
          :label-position="'top'"
        >
          <el-form-item :label="t('code')" prop="code">
            <el-input
              v-model="form.code"
              type="text"
              minlength="6"
              maxlength="6"
            />
          </el-form-item>
          <div>
            {{ t("resend-tips") }}
            <a class="resend" @click="resend">{{ t("resend") }}</a
            >{{ t("en-dot") }}
          </div>
          <el-alert
            class="tips"
            :description="t('description')"
            type="info"
            center
            :closable="false"
            :show-icon="false"
          ></el-alert>
          <el-button class="validate-button" @click="submit">Verify</el-button>
        </el-form>
      </el-card>
    </el-main>
  </el-container>
</template>
<i18n>
{
  "zh": {
    "verify": "验证账户",
    "verify-button": "验证",
    "tips": "我们已向您的邮箱发送了一封验证邮件",
    "resend": "重新发送",
    "code": "验证码",
    "description": "请填写验证码 （将在30分钟后过期）",
    "resend-failed": "重新发送失败",
    "resend-succeeded": "重新发送成功",
    "error-occurred": "发生错误",
    "resend-error": "重新发送时发生错误。请检查您的网络并重试。",
    "verify-failed": "验证失败",
    "verify-succeeded": "验证成功",
    "verify-error": "验证时发生错误。请检查您的网络并重试。",
    "rule-code": "请输入验证码",
    "rule-code-format": "请输入正确的格式",
    "resend-tips": "没有收到邮件？",
    "en-dot": ""
  },
  "en": {
    "verify": "Verify your account",
    "verify-button": "Verify",
    "code": "Code",
    "tips": "We have sent a verification mail to your email address.",
    "resend": "Resend Code",
    "description": "Please fill in the verification code, it will expire in 30 minutes.",
    "resend-failed": "Resend failed",
    "resend-succeeded": "Resend succeeded",
    "error-occurred": "Error occurred",
    "resend-error": "There was an error while resending. Please check you network and try again.",
    "verify-failed": "Verify failed",
    "verify-succeeded": "Verify succeeded",
    "verify-error": "There was an error while verifying. Please check you network and try again.",
    "rule-code": "Please input your verify code",
    "rule-code-format": "Please input the correct format",
    "resend-tips": "Didn't receive the email?",
    "en-dot": "."
  }
}
</i18n>
<style scoped>
@import "@/assets/style/user.css";

.tips {
  text-align: center;
  max-width: 280px;
  margin: 20px 0;
}

.tips strong {
  font-weight: bolder;
}

.resend {
  cursor: pointer;
}
</style>
