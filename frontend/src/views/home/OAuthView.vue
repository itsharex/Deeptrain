<script setup lang="ts">
import { ref } from "vue";
import { getWithCache } from "@/assets/script/cache";
import { useI18n } from "vue-i18n";
import { syncLangRef } from "@/assets/script/utils";
import Github from "@/components/icons/github.vue";
import { oauth } from "@/config";
import Check from "@/components/icons/home/check.vue";
import Google from "@/components/icons/google.vue";

const info = ref({
  "github": false,
  "google": false,
});
const { t, locale } = useI18n();
syncLangRef(locale);

getWithCache("oauth/list").then((resp) => {
  const data = resp.data;
  if (!data.status) ElMessage({
    type: "error",
    message: data.reason,
    showClose: false,
  });
  else info.value = data.data;
});
</script>

<template>
  <div class="form allauth">
    <div class="title"><span>{{ t("allauth") }}</span></div>
    <div class="oauth">
      <div class="app">
        <div class="logo"><github /></div>
        <div class="name">Github</div>
        <div class="grow" />
        <div class="state">
          <check v-if="info['github']" />
          <a :href="oauth.github_url" v-else>{{ t('bind') }}</a>
        </div>
      </div>
      <div class="app">
        <div class="logo"><google /></div>
        <div class="name">Google</div>
        <div class="grow" />
        <div class="state">
          <check v-if="info['google']" />
          <a :href="oauth.google_url" v-else>{{ t('bind') }}</a>
        </div>
      </div>
    </div>
  </div>
</template>
<i18n>
{
  "zh": {
    "allauth": "第三方账号",
    "bind": "前往绑定"
  },
  "en": {
    "allauth": "Third-party account",
    "bind": "Bind"
  }
}
</i18n>
<style scoped>
@import "@/assets/style/home.css";

.oauth {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin: 0 6px;
  transform: translateX(-18px);
}

.app {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 100%;
  height: max-content;
  padding: 8px 12px;
  border-radius: 4px;
  background: rgba(255, 255, 255, .05);
  cursor: pointer;
}

.logo {
  width: 32px;
  height: 32px;
  fill: #fff;
  color: #fff;
  padding: 4px;
}

.name {
  margin-left: 8px;
  font-size: 16px;
  color: #fff;
}

.state a {
  color: #fff;
  background: none;
  text-decoration: 1px underline;
  text-underline-offset: 4px;
}

.state svg {
  width: 32px;
  height: 32px;
  padding: 4px;
  transform: translateY(2px);
  fill: #70c000;
  color: #70c000;
}
</style>
