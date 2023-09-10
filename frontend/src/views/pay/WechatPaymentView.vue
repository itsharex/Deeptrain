<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { syncLangRef } from "@/assets/script/utils";
import { backend_url } from "@/config";

const { t, locale } = useI18n();
syncLangRef(locale);

const search = new URLSearchParams(location.search);
const order = search.get("id") || "";
</script>

<template>
  <el-card class="card">
    <p>
      {{ t("wechat") }}
    </p>
    <img :src="`${backend_url}qrcode/?id=${order}`" alt="qrcode" />
  </el-card>
</template>
<i18n>
{
  "zh": {
    "wechat": "请使用微信扫描下方二维码进行支付"
  },
  "en": {
    "wechat": "Please use WeChat to scan the QR code below to pay"
  }
}
</i18n>
<style scoped>
.card {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -60%);
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px 18px;
  width: max-content;
  height: max-content;
  text-align: center;
  user-select: none;
  max-width: calc(100% - 36px);
}

img {
  border-radius: 4px;
  margin-top: 24px;
  max-width: calc(100% - 24px);
}
</style>
