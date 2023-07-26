<script setup lang="ts">
import { reactive, ref } from "vue";
import type { FormRules, FormInstance } from "element-plus";
import { validateForm } from "@/assets/script/utils";
import axios from "axios";

const props = defineProps<{
  modelValue: boolean;
}>();
const emit = defineEmits(["update:modelValue"]);

const element = ref<FormInstance>();
const loading = ref<boolean>(false);

const form = reactive<Record<string, string | Record<string, any>>>({
  old: "",
  new: "",
})

const rules = reactive<FormRules>({
  old: [{ min: 6, max: 6, message: "Length should be 6", trigger: "change" }],
  new: [{ min: 6, max: 6, message: "Length should be 6", trigger: "change" }],
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
          title: "Verify failed",
          message: data.reason,
          showClose: false,
        });
      else {
        ElNotification.success({
          title: "Verify succeeded",
          message: "Please check your email to verify",
          showClose: false,
        });
        emit("update:modelValue", false);
      }
    } catch (e) {
      ElNotification.error({
        title: "Verify failed",
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
  <el-dialog v-model="props.modelValue" @close="close">
    <el-form label-width="80px" :model="form" :rules="rules" :label-position="'top'" ref="element">
      <el-form-item label="老邮箱验证码" prop="old">
        <el-input v-model="form.old" />
      </el-form-item>
      <el-form-item label="新邮箱验证码" prop="new">
        <el-input v-model="form.new" />
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
