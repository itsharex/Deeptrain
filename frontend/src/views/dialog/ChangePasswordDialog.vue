<script setup lang="ts">
import { reactive, ref } from "vue";
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
    { required: true, message: "请输入原密码", trigger: "blur" },
    { min: 6, max: 46, message: "长度应为 6 到 46", trigger: "change" },
  ],
  new_password: [
    { required: true, message: "请输入新密码", trigger: "blur" },
    { min: 6, max: 46, message: "长度应为 6 到 46", trigger: "change" },
    { validator: validateChangePassword(form), trigger: "change" },
  ],
  confirm_password: [
    { required: true, message: "请输入确认密码", trigger: "blur" },
    { min: 6, max: 46, message: "长度应为 6 到 46", trigger: "change" },
    { validator: validateRePassword(form, "new_password"), trigger: "change" },
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
          title: "修改密码失败",
          message: data.reason,
          showClose: false,
        });
      else {
        ElNotification.success({
          title: "修改密码成功",
          message: data.message,
          showClose: false,
        });
        token.value = data.token;
        close();
      }
    } catch (e) {
      ElNotification.error({
        title: "修改密码失败",
        message: "网络错误",
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
      <el-form-item label="原密码" prop="old_password">
        <el-input v-model="form.old_password" show-password></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="new_password">
        <el-input v-model="form.new_password" show-password></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="confirm_password">
        <el-input v-model="form.confirm_password" show-password></el-input>
      </el-form-item>
      <el-form-item prop="captcha">
        <gee-test id="register-captcha" v-model="captcha" />
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
