<script setup lang="ts">
import { reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import type { FormRules, FormInstance } from "element-plus";
import { validateForm } from "@/assets/script/utils";
import axios from "axios";
import { language } from "@/config";

const props = defineProps<{
  modelValue: boolean;
}>();
const emit = defineEmits(["update:modelValue"]);
const { t, locale } = useI18n();
locale.value = language.value;

const element = ref<FormInstance>();
const loading = ref<boolean>(false);

const form = reactive<Record<string, string | Record<string, any>>>({
  old: "",
  new: "",
})

const rules = reactive<FormRules>({
  old: [{ min: 6, max: 6, message: t('length-check'), trigger: "change" }],
  new: [{ min: 6, max: 6, message: t('length-check'), trigger: "change" }],
});

async function post() {
  if (loading.value) return;
  if (await validateForm(element.value)) {
    loading.value = true;
    try {
      const resp = await axios.post("/settings/verify", form),
        data = resp.data;
      if (!data.status)
        ElNotification.error({
          title: t("verify-failed"),
          message: data.reason,
          showClose: false,
        });
      else {
        ElNotification.success({
          title: t("verify-success"),
          message: t("verify-success-message"),
          showClose: false,
        });
        emit("update:modelValue", false);
      }
    } catch (e) {
      ElNotification.error({
        title: t("verify-failed"),
        message: t("network-error"),
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
  <el-dialog v-model="props.modelValue" @close="close">
    <el-form label-width="80px" :model="form" :rules="rules" :label-position="'top'" ref="element">
      <el-form-item :label="t('old')" prop="old">
        <el-input v-model="form.old" />
      </el-form-item>
      <el-form-item :label="t('new')" prop="new">
        <el-input v-model="form.new" />
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
    "change-email": "Change Email",
    "change-email-success": "Change email succeeded",
    "change-email-failed": "Change email failed",
    "network-error": "There is something wrong, please try again later",
    "length-check": "Length should be 6",
    "old": "Old Email Code",
    "new": "New Email Code",
    "verify-success": "Verify succeeded",
    "verify-failed": "Verify failed",
    "verify-success-message": "Verify succeeded! You can now use your new email to login.",
    "verify-failed-message": "Verify failed! Please check your code and try again.",
    "cancel": "Cancel",
    "confirm": "Confirm",
    "email": "Email",
    "please-input-email": "Please input email"
  },
  "zh": {
    "change-email": "修改邮箱",
    "change-email-success": "修改邮箱成功",
    "change-email-failed": "修改邮箱失败",
    "network-error": "网络错误，请稍后再试",
    "length-check": "验证码长度应为 6",
    "old": "老邮箱验证码",
    "new": "新邮箱验证码",
    "verify-success": "验证成功",
    "verify-failed": "验证失败",
    "verify-success-message": "验证成功！您现在可以使用新邮箱登录。",
    "verify-failed-message": "验证失败！请检查您的验证码并重试。",
    "cancel": "取 消",
    "confirm": "确 定",
    "email": "邮箱",
    "please-input-email": "请输入邮箱"
  }
}
</i18n>
