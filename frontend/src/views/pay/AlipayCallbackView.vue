<script setup lang="ts">
import axios from "axios";
import router from "@/router";
import BoxLoader from "@/components/BoxLoader.vue";
import { useI18n } from "vue-i18n";
import { syncLangRef } from "@/assets/script/utils";

const { t, locale } = useI18n();
syncLangRef(locale);

const param = new URLSearchParams(location.search);
const order = param.get("out_trade_no");

function refreshState() {
  axios
    .get("pay/trade?id=" + order)
    .then((res) => {
      const data = res.data;
      if (data.status) router.push("/home/wallet");
    })
    .catch((err) => {
      ElMessage({
        message: err.message,
        type: "error",
      });
    });
}

if (order == null || order.length === 0) router.push("/home/wallet");
else {
  refreshState();
  setInterval(refreshState, 2000);
}
</script>

<template>
  <div class="text">
    {{ t("wait") }}
  </div>
  <BoxLoader />
</template>

<i18n>
{
  "zh": {
    "wait": "正在等待支付结果，请耐心等待..."
  },
  "en": {
    "wait": "Waiting for payment result, please wait patiently..."
  }
}
</i18n>
<style scoped>
.text {
  position: absolute;
  top: calc(50% - 120px);
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fff;
  font-size: 18px;
  text-align: center;
  user-select: none;
  padding: 4px 8px;
}
</style>
