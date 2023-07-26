<script setup lang="ts">
import { reactive, ref } from "vue";
import GeeTest from "@/components/captcha/GeeTest.vue";
import type { FormRules, FormInstance } from "element-plus";
import { token, validateChangePassword, validateEmail, validateRePassword } from "@/assets/script/user";
import { validateForm } from "@/assets/script/utils";
import { getValidateUtilSuccess } from "@/assets/script/captcha/geetest";
import axios from "axios";
import ChangeEmailVerifyDialog from "@/views/dialog/ChangeEmailVerifyDialog.vue";

const props = defineProps<{
  modelValue: boolean;
}>();
const emit = defineEmits(["update:modelValue"]);

const element = ref<FormInstance>();
const captcha = ref<Geetest.Geetest | null>(null);
const loading = ref<boolean>(false);
const verify = ref<boolean>(false);

const form = reactive<Record<string, string | Record<string, any>>>({
  email: "",
  captcha: {},
})

const rules = reactive<FormRules>({
  email: [
    {
      type: "email",
      required: true,
      message: "Please input email",
      trigger: "blur",
    },
    { validator: validateEmail, trigger: "change" },
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
          title: "Change email failed",
          message: data.reason,
          showClose: false,
        });
      else {
        ElNotification.success({
          title: "Change email succeeded",
          message: "Please check your email to verify",
          showClose: false,
        });
        emit("update:modelValue", false);
        verify.value = true;
      }
    } catch (e) {
      ElNotification.error({
        title: "Change email failed",
        message: "There is something wrong, please try again later",
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
    <el-form label-width="80px" :model="form" :rules="rules" :label-position="'top'" ref="element">
      <el-form-item label="Email" prop="email">
        <el-input v-model="form.email" placeholder="Please input email"></el-input>
      </el-form-item>
      <el-form-item prop="captcha">
        <GeeTest v-model="captcha"  id="change-captcha"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button class="button" @click="close">取 消</el-button>
        <el-button class="button" type="primary" @click="post">确 定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped>

</style>
