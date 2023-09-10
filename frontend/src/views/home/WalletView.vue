<script setup lang="ts">
import axios from "axios";
import { useI18n } from "vue-i18n";
import { syncLangRef } from "@/assets/script/utils";
import Money from "@/components/icons/home/money.vue";
import { reactive, ref } from "vue";
import { mobile } from "@/assets/script/global";
import { getWithCache } from "@/assets/script/cache";
import { backend_url } from "@/config";
import router from "@/router";

const { t, locale } = useI18n();
syncLangRef(locale);

const balance = ref<number>(0.0);
const historyPage = ref<number>(1);
const history = ref<any[]>([]);
const form = reactive({
  type: "alipay",
  amount: 0,
});
const quickAmount = ref<number[]>([5, 10, 50, 100, 200, 500]);

function pay(amount: number) {
  axios
    .post("pay/create", {
      amount: amount,
      type: form.type,
      mobile: mobile.value,
    })
    .then((res) => {
      const data = res.data;
      if (!data.status) {
        ElMessage({
          message: data.error,
          type: "error",
        });
        return;
      }
      if (form.type === "alipay") location.href = data.url;
      if (form.type === "wechat") router.push(`/pay/wechat/order?id=${data.url}&out_trade_no=${data.order}`);
    })
    .catch((err) => {
      ElMessage({
        message: err.message,
        type: "error",
      });
    });
}

function refreshAmount() {
  getWithCache("pay/amount", 5)
    .then((res) => {
      const data = res.data;
      if (!data.status) {
        ElMessage({
          message: data.error,
          type: "error",
        });
        return;
      }
      balance.value = data.amount;
    })
    .catch((err) => {
      ElMessage({
        message: err.message,
        type: "error",
      });
    });
}

function updatePagination(current = 1) {
  getWithCache("pay/log?page=" + current, 5)
    .then((res) => {
      const data = res.data;
      if (!data.status) {
        ElMessage({
          message: data.error,
          type: "error",
        });
        return;
      }
      history.value = data.data;
      historyPage.value = data.total;
    })
    .catch((err) => {
      ElMessage({
        message: err.message,
        type: "error",
      });
    });
}

refreshAmount();
updatePagination();
setInterval(refreshAmount, 1000 * 6);
</script>

<template>
  <div class="form wallet">
    <div class="title">
      <span>{{ t("wallet") }}</span>
    </div>
    <el-card class="payment">
      <h3>{{ t("info") }}</h3>
      <div class="balance">
        <money />
        <span>{{ t("balance") }}</span>
        <p>{{ balance }} ¥</p>
      </div>
    </el-card>
    <el-card class="payment">
      <h3>充值</h3>
      <div class="pay">
        <el-radio-group v-model="form.type" style="gap: 8px">
          <el-radio label="alipay" border>{{ t("alipay") }}</el-radio>
          <el-radio label="wechat" border>{{ t("wechat") }}</el-radio>
          <el-radio label="qq" border disabled>{{ t("paypal") }}</el-radio>
        </el-radio-group>
        <div class="custom">
          <el-input-number
            class="amount"
            v-model="form.amount"
            :min="0.01"
            :max="20000"
            :precision="2"
            controls-position="right"
          />
          <el-button class="button" type="primary" @click="pay(form.amount)">{{
            t("pay")
          }}</el-button>
        </div>
        <div class="quick">
          <el-button
            v-for="amount in quickAmount"
            :key="amount"
            @click="pay(amount)"
            >{{ amount }} ¥</el-button
          >
        </div>
      </div>
    </el-card>
  </div>
  <div class="form history">
    <div class="title">
      <span>{{ t("history") }}</span>
    </div>
    <el-card class="table">
      <el-table
        :data="history"
        :empty-text="t('no-data')"
        style="border-radius: 4px"
      >
        <el-table-column prop="order" :label="t('order')" />
        <el-table-column prop="time" :label="t('time')" />
        <el-table-column prop="amount" :label="t('amount')" />
        <el-table-column prop="type" :label="t('type')">
          <template #default="{ row }">
            <span>
              {{ t(`${row.type}`) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="state" :label="t('state')">
          <template #default="{ row }">
            <el-tag
              :type="row.state == true ? 'success' : 'warning'"
              size="small"
              >{{ t(`pay-${row.state}`) }}</el-tag
            >
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        class="pagination"
        layout="prev, pager, next"
        :page-count="historyPage"
        @current-change="updatePagination"
      />
    </el-card>
  </div>
</template>
<i18n>
{
  "en": {
    "wallet": "Wallet",
    "info": "Info",
    "balance": "Balance",
    "alipay": "Alipay",
    "wechat": "WeChat Pay",
    "paypal": "PayPal",
    "pay": "Pay",
    "history": "Payment History",
    "order": "Order",
    "time": "Time",
    "amount": "Amount",
    "type": "Type",
    "state": "State",
    "no-data": "No Data",
    "pay-true": "Paid",
    "pay-false": "Unpaid"
  },
  "zh": {
    "wallet": "钱包",
    "info": "信息",
    "balance": "余额",
    "alipay": "支付宝",
    "wechat": "微信支付",
    "paypal": "PayPal 境外支付",
    "pay": "支付",
    "history": "充值记录",
    "order": "订单",
    "time": "时间",
    "amount": "金额",
    "type": "类型",
    "state": "状态",
    "no-data": "暂无数据",
    "pay-true": "已支付",
    "pay-false": "未支付"
  }
}
</i18n>
<style scoped>
@import "@/assets/style/home.css";

.payment {
  margin: 24px 0;
  width: calc(100% - 32px);
  height: max-content;
}

.payment h3 {
  margin: 0 8px;
  font-size: 20px;
  font-weight: bold;
  user-select: none;
}

.table {
  width: calc(100% - 32px);
  margin: 16px 0;
}

.balance {
  display: flex;
  flex-direction: row;
  align-items: center;
  font-size: 18px;
  margin: 24px 8px;
  user-select: none;
  gap: 8px;
}

.balance svg {
  margin: 2px;
  width: 24px;
  height: 24px;
  fill: #eee;
}

.balance p {
  margin: 0 8px;
  font-weight: bold;
  font-size: 20px;
}

.pay {
  display: flex;
  flex-direction: column;
  font-size: 18px;
  margin: 24px 8px;
  padding: 4px;
  user-select: none;
  gap: 12px;
}

.custom {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 6px;
  margin: 4px 0;
  width: 100%;
}

.custom .amount {
  flex-grow: 1;
  max-width: 361px;
}

.custom .button {
  width: 80px;
}

.quick {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 4px;
}

.history {
  margin-top: 58px;
}

.pagination {
  width: max-content;
  margin: 28px 6px 8px auto;
}
</style>
