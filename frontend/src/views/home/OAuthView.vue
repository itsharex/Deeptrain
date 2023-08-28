<script setup lang="ts">
import "axios";
import { reactive, ref } from "vue";
import { getWithCache } from "@/assets/script/cache";
import { useI18n } from "vue-i18n";
import { copyClipboard, syncLangRef, validateForm } from "@/assets/script/utils";
import Github from "@/components/icons/github.vue";
import { oauth } from "@/config";
import Check from "@/components/icons/home/check.vue";
import Google from "@/components/icons/google.vue";
import type { FormInstance, FormRules } from "element-plus";
import GeeTest from "@/components/captcha/GeeTest.vue";
import { getValidateUtilSuccess } from "@/assets/script/captcha/geetest";
import axios from "axios";
import { mobile } from "@/assets/script/global";

const captcha = ref<Geetest.Geetest | null>(null);
const info = ref({
  "github": false,
  "google": false,
});
const { t, locale } = useI18n();
syncLangRef(locale);

const state = reactive<Record<string, any>>({
  state: 0,
  name: "",
  no: "",
  link: "",
});
const dialog = ref(false);

const form = reactive({
  name: "",
  id: "",
  captcha: {},
})

const element = ref<FormInstance>();
const rules = reactive<FormRules>({
  name: [
    { required: true, message: "请输入姓名", trigger: "blur" },
    { min: 2, max: 26, message: "姓名与格式不符", trigger: "change" },
  ],
  id: [
    { required: true, message: "请输入身份证号", trigger: "blur" },
    { min: 18, max: 18, message: "身份证号与格式不符", trigger: "change" },
  ],
  captcha: [{ required: true, message: "", trigger: "blur" }],
});

getWithCache("oauth/list").then((resp) => {
  const data = resp.data;
  if (!data.status) ElMessage({
    type: "error",
    message: data.reason,
    showClose: false,
  });
  else info.value = data.data;
});

async function submit() {
  if (await validateForm(element.value)) {
    form.captcha = await getValidateUtilSuccess(captcha.value);
    axios.post("cert/request", form)
    .then((resp) => {
      const data = resp.data;
      if (!data.status) ElMessage({
        type: "error",
        message: data.error,
        showClose: false,
      });
      else {
        state.state = 1;
        state.name = form.name;
        state.no = form.id;
        state.link = data.uri;
        console.debug("cert: ", state.link);
      }
    })
    .catch((err) => {
      ElMessage({
        type: "error",
        message: err.message,
        showClose: false,
      });
    });
  }
}

function refreshState(updater = true) {
  if (state.state === 2) return;
  if (updater && state.state === 0) return;
  axios.get("cert/state")
    .then((resp) => {
      const data = resp.data;
      for (const key in data) state[key] = data[key];
    })
    .catch((err) => {
      ElMessage({
        type: "error",
        message: err.message,
        showClose: false,
      });
    });
}

function copy() {
  copyClipboard(state.link);
  ElMessage({
    type: "success",
    message: "已复制到剪贴板",
    showClose: false,
  });

  dialog.value = false;
}

function goto() {
  location.href = state.link;
  dialog.value = false;
}

refreshState(false);
setInterval(refreshState, 1000 * 10);
</script>

<template>
  <el-dialog
    v-model="dialog"
    title="前往身份认证"
    width="30%"
    align-center
  >
    <span>您将前往支付宝进行身份认证，请注意，认证功能需要在手机端进行，如果您当前的设备为电脑端，请复制下方链接到手机端进行认证。</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="copy">我是电脑，复制链接</el-button>
        <el-button type="primary" @click="goto">我是手机，前往认证</el-button>
      </span>
    </template>
  </el-dialog>
  <div class="form cert">
    <div class="title"><span>{{ t('cert') }}</span></div>
    <el-form class="cert-form" ref="element" :model="form" :rules="rules" :label-position="'left'" label-width="80px" v-if="state.state === 0">
      <el-form-item label="姓名" prop="name">
        <el-input v-model="form.name" maxlength="26" />
      </el-form-item>
      <el-form-item label="身份证号" prop="id">
        <el-input v-model="form.id" maxlength="18" />
      </el-form-item>
      <el-form-item prop="captcha">
        <gee-test id="cert-captcha" v-model="captcha" />
      </el-form-item>
      <el-button style="margin: 0 auto" @click="submit">开始验证</el-button>
    </el-form>
    <el-card v-else class="cert-card">
      <el-descriptions title="认证信息" :column="mobile ? 1 : 2">
        <el-descriptions-item label="认证姓名">{{ state.name }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ state.no }}</el-descriptions-item>
        <el-descriptions-item label="认证类型">个人认证</el-descriptions-item>
        <el-descriptions-item label="认证状态">
          <el-tag type="warning" v-if="state.state === 1">未认证</el-tag>
          <el-tag type="success" v-else>已实名</el-tag>
        </el-descriptions-item>
      </el-descriptions>
      <div class="privacy">
        认证即代表您同意
        <a href="https://render.alipay.com/p/yuyan/180020010001196791/preview.html?agreementId=AG00000132" target="_blank">
          《支付宝实名认证隐私政策》
        </a>
      </div>
      <div class="cert-button" v-if="state.state === 1">
        <el-button type="primary" @click="dialog = true">前往认证</el-button>
        <el-button type="primary" plain @click="state.state = 0">重新认证</el-button>
      </div>
    </el-card>
  </div>
  <br>
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
    "cert": "实名认证",
    "allauth": "第三方账号",
    "bind": "前往绑定"
  },
  "en": {
    "cert": "Certification (Chinese only)",
    "allauth": "Third-party account",
    "bind": "Bind"
  }
}
</i18n>
<style scoped>
@import "@/assets/style/home.css";

.cert-form {
  display: flex;
  flex-direction: column;
  max-width: 380px;
  width: calc(100% - 32px);
  margin: 38px auto 24px;
  align-items: center;
}

.cert-form div {
  width: 100%;
}

.cert-card {
  width: calc(100% - 16px);
  user-select: none;
  background: rgba(255, 255, 255, .05);
}

.privacy {
  width: max-content;
  margin: 24px auto 12px;
}

.privacy a {
  margin: 0 !important;
  transform: translateX(-4px);
}

.cert-button {
  width: max-content;
  margin: 16px auto 8px;
}

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
