<script setup lang="ts">
import { RouterLink } from "vue-router";
import { token } from "@/assets/script/user";
import { refreshState } from "@/assets/script/global";
import router from "@/router";
import { useI18n } from "vue-i18n";
import { language } from "@/config";

const { t, locale } = useI18n();
locale.value = language.value;

async function submit() {
  token.value = "";
  refreshState();
  await router.push("/");
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
      <h1>{{ t("logout") }}</h1>
      <el-card shadow="hover">
        <div class="tips">{{ t("tips") }}</div>
        <el-button class="validate-button" @click="submit">{{
          t("confirm")
        }}</el-button>
      </el-card>
    </el-main>
  </el-container>
</template>
<i18n>
{
  "zh": {
    "logout": "退出登录",
    "tips": "是否确认退出登录？",
    "confirm": "确定"
  },
  "en": {
    "logout": "Logout",
    "tips": "Are you sure to log out?",
    "confirm": "Confirm"
  }
}
</i18n>
<style scoped>
@import "@/assets/style/user.css";

.tips {
  text-align: center;
  max-width: 280px;
  margin: 20px 30px 50px;
}
</style>
