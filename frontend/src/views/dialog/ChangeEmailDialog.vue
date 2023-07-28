<script setup lang="ts">
import { reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import GeeTest from "@/components/captcha/GeeTest.vue";
import type { FormRules, FormInstance } from "element-plus";
import { validateEmail } from "@/assets/script/user";
import { validateForm } from "@/assets/script/utils";
import { getValidateUtilSuccess } from "@/assets/script/captcha/geetest";
import axios from "axios";
import ChangeEmailVerifyDialog from "@/views/dialog/ChangeEmailVerifyDialog.vue";
import { language } from "@/config";

const props = defineProps<{
  modelValue: boolean;
}>();
const emit = defineEmits(["update:modelValue"]);
const { t, locale } = useI18n();
locale.value = language.value;

const element = ref<FormInstance>();
const captcha = ref<Geetest.Geetest | null>(null);
const loading = ref<boolean>(false);
const verify = ref<boolean>(false);

const form = reactive<Record<string, string | Record<string, any>>>({
  email: "",
  captcha: {},
});

const rules = reactive<FormRules>({
  email: [
    {
      type: "email",
      required: true,
      message: t("please-input-email"),
      trigger: "blur",
    },
    { validator: validateEmail(t), trigger: "change" },
  ],
  captcha: [{ required: true, message: "", trigger: "blur" }],
});

async function post() {
  if (loading.value) return;
  if (await validateForm(element.value)) {
    form.captcha = await getValidateUtilSuccess(captcha.value);
    loading.value = true;
    try {
      const resp = await axios.post("/settings/email", form),
        data = resp.data;
      if (!data.status)
        ElNotification.error({
          title: t("change-email-failed"),
          message: data.reason,
          showClose: false,
        });
      else {
        ElNotification.success({
          title: t("change-email-success"),
          message: t("please-check-email"),
          showClose: false,
        });
        emit("update:modelValue", false);
        verify.value = true;
      }
    } catch (e) {
      ElNotification.error({
        title: t("network-error"),
        message: t("change-email-failed"),
        showClose: false,
      });
    } finally {
      loading.value = false;
    }
  }
}

function close() {
  emit("update:modelValue", false);
}
</script>
<template>
  <ChangeEmailVerifyDialog v-model="verify" />
  <el-dialog v-model="props.modelValue" @close="close">
    <el-form
      label-width="80px"
      :model="form"
      :rules="rules"
      :label-position="'top'"
      ref="element"
    >
      <el-form-item :label="t('email')" prop="email">
        <el-input
          v-model="form.email"
          :placeholder="t('please-input-email')"
        ></el-input>
      </el-form-item>
      <el-form-item prop="captcha">
        <GeeTest v-model="captcha" id="change-captcha" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button class="button" @click="close">{{ t("cancel") }}</el-button>
        <el-button class="button" type="primary" @click="post">{{
          t("confirm")
        }}</el-button>
      </span>
    </template>
  </el-dialog>
</template>
<i18n>
{
  "en": {
    "change-email": "Change Email",
    "change-email-success": "Change email succeeded",
    "change-email-failed": "Change email failed",
    "network-error": "There is something wrong, please try again later",
    "email": "Email",
    "please-input-email": "Please input email",
    "please-check-email": "Please check your email to verify",
    "cancel": "Cancel",
    "confirm": "Confirm",
    "user.email-format-error": "The format of the email is incorrect",
    "user.email-format-unsupported": "Please use a supported email suffix"
  },
  "zh": {
    "change-email": "修改邮箱",
    "change-email-success": "修改邮箱成功",
    "change-email-failed": "修改邮箱失败",
    "network-error": "网络错误，请稍后再试",
    "email": "邮箱",
    "please-input-email": "请输入邮箱",
    "please-check-email": "请检查邮箱以验证",
    "cancel": "取 消",
    "confirm": "确 定",
    "user.email-format-error": "邮箱格式不正确",
    "user.email-format-unsupported": "邮箱后缀不支持，请使用支持的邮箱后缀"
  }
}
</i18n>
