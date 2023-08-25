<script setup lang="ts">
import { username } from "@/assets/script/global";
import router from "@/router";
import { language } from "@/config";
import { useI18n } from "vue-i18n";
import General from "@/components/icons/home/general.vue";
import Tab from "@/components/Tab.vue";
import Oauth from "@/components/icons/home/oauth.vue";

const { t, locale } = useI18n();
locale.value = language.value;

function logout() {
  router.push("/logout");
}
</script>
<template>
  <el-container>
    <el-main>
      <el-card class="card">
        <div class="header">
          <div class="logo">
            <img src="/favicon.ico" alt="" />
            <span>{{ t("title") }}</span>
          </div>
          <div class="grow" />
          <div class="username">{{ username }}</div>
          <div class="logout" @click="logout">{{ t("logout") }}</div>
        </div>
      </el-card>
      <el-container class="section">
        <div class="router">
          <Tab to="/home"><general /></Tab>
          <Tab to="/home/oauth"><oauth /></Tab>
        </div>
        <el-card class="view">
          <router-view />
        </el-card>
      </el-container>
    </el-main>
  </el-container>
</template>
<i18n>
{
  "en": {
    "title": "Deeptrain",
    "logout": "Logout"
  },
  "zh": {
    "title": "Deeptrain 账号管理",
    "logout": "退出登录"
  }
}
</i18n>
<style scoped>
@import "@/assets/style/anim.css";

.card {
  width: 100%;
  max-width: 820px;
  margin: 8px auto 12px;
  animation: FadeInAnimation 1s;
}

.section {
  display: flex;
  flex-direction: row;
  width: 100%;
  max-width: 820px;
  margin: 8px auto 12px;
}

.view {
  flex-grow: 1;
}

.router {
  display: flex;
  flex-direction: column;
  width: min-content;
  margin-right: 6px;
}

.header {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.logo {
  width: max-content;
  height: max-content;
  user-select: none;
  display: flex;
  align-items: center;
}

.logo img {
  width: 36px;
  height: 36px;
}

.logo span {
  font-size: 24px;
  font-weight: 600;
  margin-left: 16px;
  color: rgba(255, 255, 255, 0.9);
}

.username {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin-right: 16px;
  user-select: none;
  white-space: nowrap;
}

.logout {
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.2);
  padding: 8px 16px;
  border-radius: 4px;
  transition: 0.5s;
  user-select: none;
  white-space: nowrap;
}

.logout:hover {
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 620px) {
  .logo span {
    display: none;
  }
}

@media (max-width: 540px) {
  .username {
    display: none;
  }
}
</style>
