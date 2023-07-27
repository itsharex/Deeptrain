<script setup lang="ts">
import { reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import GeeTest from "@/components/captcha/GeeTest.vue";
import type { FormRules, FormInstance } from "element-plus";
import { token, validateChangePassword, validateRePassword } from "@/assets/script/user";
import { validateForm } from "@/assets/script/utils";
import { getValidateUtilSuccess } from "@/assets/script/captcha/geetest";
import axios from "axios";

const props = defineProps<{
  modelValue: boolean;
}>();
const emit = defineEmits(["update:modelValue"]);
const { t } = useI18n();

const element = ref<FormInstance>();
const captcha = ref<Geetest.Geetest | null>(null);
const loading = ref<boolean>(false);

const form = reactive<Record<string, string | Record<string, any>>>({
  old_password: "",
  new_password: "",
  confirm_password: "",
  captcha: {},
})

const rules = reactive<FormRules>({
  old_password: [
    { required: true, message: t('rule-old-password'), trigger: "blur" },
    { min: 6, max: 46, message: t('rule-password-length'), trigger: "change" },
  ],
  new_password: [
    { required: true, message: t('rule-new-password'), trigger: "blur" },
    { min: 6, max: 46, message: t('rule-password-length'), trigger: "change" },
    { validator: validateChangePassword(t, form), trigger: "change" },
  ],
  confirm_password: [
    { required: true, message: t('rule-confirm-password'), trigger: "blur" },
    { min: 6, max: 46, message: t('rule-password-length'), trigger: "change" },
    { validator: validateRePassword(t, form, "new_password"), trigger: "change" },
  ],
  captcha: [{ required: true, message: "", trigger: "blur" }],
});

async function post() {
  if (loading.value) return;
  if (await validateForm(element.value)) {
    form.captcha = await getValidateUtilSuccess(captcha.value);
    loading.value = true;
    try {
      const resp = await axios.post("/settings/password", {
          old: form.old_password,
          new: form.new_password,
          confirm: form.confirm_password,
          captcha: form.captcha,
        }),
        data = resp.data;
      if (!data.status)
        ElNotification.error({
          title: t("change-failed"),
          message: data.reason,
          showClose: false,
        });
      else {
        ElNotification.success({
          title: t("change-succeeded"),
          message: data.message,
          showClose: false,
        });
        token.value = data.token;
        close();
      }
    } catch (e) {
      ElNotification.error({
        title: t("change-failed"),
        message: t("network-error"),
        showClose: false,
      });
    }
    loading.value = false;
  }
}

function close() {
  emit("update:modelValue", false);
}
</script>

<template>
  <el-dialog v-model="props.modelValue" @close="close">
    <el-form label-width="80px" :model="form" :rules="rules" :label-position="'top'" ref="element">
      <el-form-item :label="t('old-password')" prop="old_password">
        <el-input v-model="form.old_password" show-password></el-input>
      </el-form-item>
      <el-form-item :label="t('new-password')" prop="new_password">
        <el-input v-model="form.new_password" show-password></el-input>
      </el-form-item>
      <el-form-item :label="t('confirm-password')" prop="confirm_password">
        <el-input v-model="form.confirm_password" show-password></el-input>
      </el-form-item>
      <el-form-item prop="captcha">
        <gee-test id="change-password-captcha" v-model="captcha" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button class="button" @click="close">{{ t('cancel') }}</el-button>
        <el-button class="button" type="primary" @click="post">{{ t('confirm') }}</el-button>
      </span>
    </template>
  </el-dialog>
</template>
<i18n>
{
  "en": {
    "old-password": "Old Password",
    "new-password": "New Password",
    "confirm-password": "Confirm Password",
    "cancel": "Cancel",
    "confirm": "Confirm",
    "change-password": "Change Password",
    "change-failed": "Change Password Failed",
    "change-succeeded": "Change Password Succeeded",
    "change-message": "Please input your new password",
    "change-success-message": "Your password has been changed successfully",
    "network-error": "There was an error while changing password. Please check you network and try again.",
    "rule-old-password": "Please input your old password",
    "rule-new-password": "Please input your new password",
    "rule-confirm-password": "Please input your confirm password",
    "rule-password": "Please input your password",
    "rule-re-password": "Please input your password again",
    "rule-password-not-match": "The two passwords you entered do not match",
    "rule-password-length": "Length should be 6 to 46",
    "user.rule-password-not-different": "The new password cannot be the same as the old password",
    "user.rule-password-not-same": "The password does not match"
  },
  "zh": {
    "old-password": "原密码",
    "new-password": "新密码",
    "confirm-password": "确认密码",
    "cancel": "取消",
    "confirm": "确定",
    "change-password": "修改密码",
    "change-failed": "修改密码失败",
    "change-succeeded": "修改密码成功",
    "change-message": "请输入新密码",
    "change-success-message": "您的密码已成功修改",
    "network-error": "修改密码失败，请检查您的网络并重试",
    "rule-old-password": "请输入原密码",
    "rule-new-password": "请输入新密码",
    "rule-confirm-password": "请输入确认密码",
    "rule-password": "请输入密码",
    "rule-re-password": "请再次输入密码",
    "rule-password-not-match": "两次输入的密码不一致",
    "rule-password-length": "长度应为 6 到 46",
    "user.rule-password-not-different": "新密码不能与原密码相同",
    "user.rule-password-not-same": "两次输入的密码不一致"
  }
}
</i18n>
