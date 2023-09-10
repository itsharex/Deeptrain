<script setup lang="ts">
import Gift from "@/components/icons/home/gift.vue";
import { useI18n } from "vue-i18n";
import { syncLangRef } from "@/assets/script/utils";
import { reactive } from "vue";
import { getWithCache } from "@/assets/script/cache";
import Chatnio from "@/components/icons/app/chatnio.vue";

const { t, locale } = useI18n();
syncLangRef(locale);

const state = reactive<Record<string, any>>({
  cert: false,
  minority: false,
});

function refreshState() {
  getWithCache("package/state", 10)
    .then((resp) => {
      const data = resp.data;
      if (!data.status)
        ElMessage({
          type: "error",
          message: data.reason,
          showClose: false,
        });
      else {
        for (const key in data.data) state[key] = data.data[key];
      }
    })
    .catch((err) => {
      ElMessage({
        type: "error",
        message: err,
        showClose: false,
      });
    });
}

refreshState();
setInterval(refreshState, 1000 * 20);
</script>

<template>
  <el-card class="package-card">
    <div class="title">
      <gift />
      <span>{{ t("package-cert") }}</span>
      <el-tag class="tag" v-if="state.cert" type="success">{{
        t("success")
      }}</el-tag>
      <el-tag class="tag" v-else type="warning">{{ t("unclaimed") }}</el-tag>
    </div>
    <el-alert
      class="alert"
      type="warning"
      v-if="!state.cert"
      show-icon
      :closable="false"
    >
      <span>{{ t("unclaimed-desc-before") }}</span>
      <router-link to="/home/oauth" style="position: relative; top: -1px">{{
        t("cert")
      }}</router-link>
      <span style="position: relative; top: -1px">{{
        t("unclaimed-desc-after")
      }}</span>
    </el-alert>
    <div class="wrapper">
      <div class="app">
        <div class="icon"><img src="/chatnio.png" alt="" /></div>
        <div class="content">
          <a href="https://chatnio.net" target="_blank" class="name">chatnio</a>
          <div class="description">
            <p>赠送 <chatnio /> 50</p>
          </div>
        </div>
      </div>
    </div>
  </el-card>

  <el-card class="package-card">
    <div class="title">
      <gift />
      <span>{{ t("package-minority") }}</span>
      <el-tag class="tag" v-if="state.minority" type="success">{{
        t("success")
      }}</el-tag>
      <el-tag class="tag" v-else type="warning">{{ t("unclaimed") }}</el-tag>
    </div>
    <el-alert
      class="alert"
      type="warning"
      v-if="!state.minority"
      show-icon
      :closable="false"
    >
      <span>{{ t("minority-desc") }}</span>
    </el-alert>
    <div class="wrapper">
      <div class="app">
        <div class="icon"><img src="/chatnio.png" alt="" /></div>
        <div class="content">
          <a href="https://chatnio.net" target="_blank" class="name">chatnio</a>
          <div class="description">
            <p>赠送 <chatnio /> 150</p>
          </div>
        </div>
      </div>
    </div>
  </el-card>
</template>
<i18n>
{
  "zh": {
    "package-cert": "实名认证礼包",
    "package-minority": "未成年人优惠",
    "success": "已领取",
    "unclaimed": "未领取",
    "unclaimed-desc-before": "您需要完成",
    "cert": "实名认证",
    "unclaimed-desc-after": "才能领取礼包",
    "minority-desc": "您需要完成实名认证且身份证上的年龄应小于或等于 18 周岁才可领取福利"
  },
  "en": {
    "package-cert": "Certification Package",
    "package-minority": "Minority Discount",
    "success": "Success",
    "unclaimed": "Unclaimed",
    "unclaimed-desc-before": "You need to complete ",
    "cert": "certification",
    "unclaimed-desc-after": " to claim the package",
    "minority-desc": "You need to complete certification and the age on your ID card should be less than or equal to 18 years old to claim the package"
  }
}
</i18n>
<style scoped>
.package-card {
  width: 100%;
  height: max-content;
  padding: 8px 6px;
  margin: 16px 0;
}

.title {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
  user-select: none;
  margin-bottom: 12px;
}

.title svg {
  width: 24px;
  height: 24px;
  margin-right: 8px;
  fill: #eee;
}

.tag {
  margin: 2px 12px;
  user-select: none;
  transform: translateY(1px);
}

.wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: max-content;
}

.app {
  display: flex;
  flex-direction: row;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 4px;
  gap: 16px;
}

.app .icon img {
  width: 46px;
  height: 46px;
}

.alert {
  display: flex;
  flex-direction: row;
  margin-bottom: 8px;
}

.app .content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.app .content .name {
  font-size: 20px;
  font-weight: bold;
  user-select: none;
  background: none !important;
  padding: 0 !important;
}

.app .content .description {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.app .content .description p {
  display: flex;
  flex-direction: row;
  align-items: center;
  user-select: none;
}

.app .content .description p svg {
  width: 18px;
  height: 18px;
  fill: #eee;
  margin: 0 6px;
}

.description p {
  margin: 0;
  font-size: 16px;
}

.description p::before {
  content: "";
  display: inline-block;
  top: 1px;
  left: -2px;
  width: 3px;
  height: 18px;
  background: #409eff;
  margin-right: 8px;
  border-radius: 2px;
  user-select: none;
}
</style>
