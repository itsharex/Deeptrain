<script setup lang="ts">
import type { FormInstance, FormRules } from "element-plus";
import { RouterLink } from "vue-router";
import { reactive, ref } from "vue";
import axios from "axios";
import Github from "@/components/icons/github.vue";
import Gitee from "@/components/icons/gitee.vue";
import OLink from "@/components/oauth/olink.vue";
import { validateForm } from "@/assets/script/utils";
import { token } from "@/assets/script/user";

const element = ref<FormInstance>();
const loading = ref<boolean>(false);
const error = ref<string>("");
const form = reactive({
  code: "",
});

const rules = reactive<FormRules>({
  username: [
    { required: true, message: 'Please input your verify code', trigger: 'blur' },
    { min: 6, max: 6, message: 'Length should be 6', trigger: 'change' },
  ],
})

async function submit(e: Event) {
  if (await validateForm(element.value)) {
    loading.value = true;
    try {
      const resp = await axios.post('login', form), data = resp.data;
      if (!data.status) ElNotification.error({
        title: "Login failed",
        message: data.reason,
        showClose: false,
      });
      else {
        token.value = data.token;
        ElNotification.success({
          title: "Login succeeded",
          message: `Welcome back ${form.username} !`,
          showClose: false,
        });
      }
    } catch (e) {
      ElNotification.warning({
        title: "Error occurred",
        message: "There was an error while logging in. Please check you network and try again.",
        showClose: false,
      });
    }
    loading.value = false;
  }
}
</script>

<template>
  <el-container>
    <el-header>
      <RouterLink to="/" class="header">
        <img src="/favicon.ico" alt="Deeptrain">
      </RouterLink>
    </el-header>
    <el-main class="main">
      <h1>Sign in to Deeptrain</h1>
      <el-card shadow="hover" v-loading="loading">
        <el-form ref="element" :model="form" :rules="rules" :label-position="'top'">
          <el-form-item label="Username" prop="code">
            <el-input v-model="form.code" type="text" minlength="6" maxlength="6" />
          </el-form-item><br>
          <el-button class="validate-button" @click="submit">Verify</el-button>
        </el-form>
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>
@import "@/assets/sytle/user.css";
</style>
