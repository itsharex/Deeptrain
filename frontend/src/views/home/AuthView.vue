<script setup lang="ts">
import "axios";
import "@/assets/style/home.css";
import { onMounted, reactive, ref, watch } from "vue";
import { getWithCache } from "@/assets/script/cache";
import { useI18n } from "vue-i18n";
import { syncLangRef } from "@/assets/script/utils";
import axios from "axios";
import { backend_url } from "@/config";

const { t, locale } = useI18n();
syncLangRef(locale);

const state = reactive<Record<string, any>>({
  tfa: false,
  fa_qrcode: "",
  fa_code: ""
})

const dialog = ref<boolean>(false);

async function tfaChanged(value: boolean) {
  if (value) {
    const resp = await getWithCache("2fa/enable", 10), data = resp.data;
    if (data.status) {
      state.fa_qrcode = data.url;
    } else {
      ElMessage({
        type: "error",
        message: data.reason,
      });
    }
  } else {
    const resp = await getWithCache("2fa/disable", 10), data = resp.data;
    if (!data.status) {
      ElMessage({
        type: "error",
        message: data.reason,
      });
    } else {
      state.tfa = false;
    }
  }
}

async function tfaActivate() {
  const resp = await getWithCache(`2fa/activate?secret=${state.fa_code}`, 2), data = resp.data;
  if (!data.status) {
    ElMessage({
      type: "error",
      message: data.reason,
    });
  } else {
    state.tfa = true;
    state.fa_qrcode = "";
    state.fa_code = "";
    dialog.value = false;
  }
}

function tfaRemoved() {
  state.fa_qrcode = "";
}

onMounted(() => {
  getWithCache("2fa/state").then((res) => state.tfa = res.data.enabled);
});
</script>

<template>
  <el-dialog v-model="dialog" :title="t('2fa-title')">
    <el-form>
      <el-form-item :label="t('2fa-code')">
        <el-input
          class="tfa-input"
          v-model="state.fa_code"
          maxlength="6"
          minlength="6"
          :parser="(value: string) => value.replace(/[^0-9]/g, '')"
          :formatter="(value: string) => value.replace(/[^0-9]/g, '')"
          :placeholder="t('2fa-code')"
        />
      </el-form-item>
      <span class="tfa">{{ t('2fa-description') }}</span>
    </el-form>
    <template #footer>
      <span>
        <el-button type="primary" @click="tfaActivate" :disabled="state.fa_code.length !== 6">
          {{ t("2fa-submit") }}
        </el-button>
      </span>
    </template>
  </el-dialog>
  <div class="form auth">
    <div class="title">
      <span>{{ t("auth") }}</span>
      <el-form class="auth-form flex-form" label-position="left">
        <el-form-item :label="t('2fa')">
          <el-switch :model-value="state.tfa" @change="tfaChanged" />
        </el-form-item>
        <template v-if="state.fa_qrcode.length > 0 && !state.tfa">
          <div class="qrcode">
            <img :src="`${backend_url}qrcode/?id=${state.fa_qrcode}`" alt="qrcode" />
          </div>
          <p class="step">{{ t("step") }}</p>
          <p class="tip">{{ t("tip") }}</p>
          <div class="action">
            <el-button @click="tfaRemoved">{{ t("cancel") }}</el-button>
            <el-button type="primary" @click="dialog = true">{{ t("verify") }}</el-button>
          </div>
        </template>
      </el-form>
    </div>
  </div>
  <br />
</template>
<i18n>
{
  "zh": {
    "auth": "身份验证",
    "2fa": "双因子认证",
    "step": "请使用双因子认证器扫描下方二维码",
    "tip": "如「Google Authenticator」、「1Password」等",
    "cancel": "取消",
    "verify": "验证",
    "2fa-title": "2FA 验证",
    "2fa-description": "请输入您刚刚扫描到的 2FA 验证器中的验证码",
    "2fa-code": "验证码",
    "2fa-submit": "验证"
  },
  "en": {
    "auth": "Authentication",
    "2fa": "Two-factor authentication",
    "step": "Please use the two-factor authenticator to scan the QR code below",
    "tip": "Such as 「Google Authenticator」、「1Password」, etc.",
    "cancel": "Cancel",
    "verify": "Verify",
    "2fa-title": "2FA Verification",
    "2fa-description": "Please enter the verification code in your 2FA authenticator",
    "2fa-code": "Verification Code",
    "2fa-submit": "Verify"
  }
}
</i18n>
<style scoped>
.auth-form {
  display: flex;
  flex-direction: column;
  width: calc(100% - 32px);
  margin: 24px 0;
}

.qrcode {
  margin: 24px auto 4px;
  max-width: calc(100% - 32px);
  width: max-content;
  height: max-content;
}

.qrcode img {
  width: 100%;
  height: 100%;
  border-radius: 4px;
}

.step {
  font-size: 16px;
  text-align: center;
  margin-top: 16px;
}

.tip {
  font-size: 12px;
  text-align: center;
  margin-top: 4px;
}

.action {
  margin-top: 16px;
}

.tfa {
  display: flex;
  user-select: none;
  justify-content: center;
  text-align: center;
  margin: 12px auto;
}
</style>
