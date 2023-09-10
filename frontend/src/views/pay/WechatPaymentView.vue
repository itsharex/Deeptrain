<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { syncLangRef } from "@/assets/script/utils";
import { backend_url } from "@/config";
import axios from "axios";
import router from "@/router";

const { t, locale } = useI18n();
syncLangRef(locale);

const search = new URLSearchParams(location.search);
const link = search.get("id") || "";
const order = search.get("out_trade_no") || "";

function goto_wechat() {
  location.href = "weixin://";
}

setInterval(() => {
  axios
    .get("pay/trade?id=" + order)
    .then((res) => {
      if (res.data.status) {
        ElMessage({
          type: "success",
          message: t("pay_success"),
        });
        router.push("/home/wallet");
      }
    })
}, 5000);
</script>

<template>
  <el-card class="wechat-card">
    <p>
      {{ t("wechat") }}
    </p>
    <img :src="`${backend_url}qrcode/?id=${link}`" alt="qrcode" />
    <el-button type="primary" @click="goto_wechat">
      {{ t("go") }}
    </el-button>
  </el-card>
</template>
<i18n>
{
  "zh": {
    "wechat": "请使用微信扫描下方二维码进行支付",
    "go": "打开微信",
    "pay_success": "支付成功！"
  },
  "en": {
    "wechat": "Please use WeChat to scan the QR code below to pay",
    "go": "Open WeChat",
    "pay_success": "Payment successful!"
  }
}
</i18n>
<style>
.wechat-card {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -60%);
  padding: 12px 18px;
  width: max-content;
  height: max-content;
  user-select: none;
  max-width: calc(100% - 36px);
}

.wechat-card .el-card__body {
  display: flex;
  flex-direction: column;
  gap: 6px;
  text-align: center;
  align-items: center;
  justify-content: center;
}

.wechat-card img {
  border-radius: 4px;
  margin: 24px 0;
  max-width: calc(100% - 24px);
}
</style>
