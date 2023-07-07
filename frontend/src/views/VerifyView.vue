<script setup lang="ts">
import type { FormInstance, FormRules } from "element-plus";
import { RouterLink } from "vue-router";
import { reactive, ref } from "vue";
import axios from "axios";
import { validateForm } from "@/assets/script/utils";
import { token } from "@/assets/script/user";
import router from "@/router";
import { state } from "@/assets/script/global";
import { app } from "@/assets/script/allauth";

const element = ref<FormInstance>();
const loading = ref<boolean>(false);
const form = reactive({
  code: "",
});

const rules = reactive<FormRules>({
  code: [
    {
      required: true,
      message: "Please input your verify code",
      trigger: "blur",
    },
    {
      min: 6,
      max: 6,
      message: "Please input the correct format",
      trigger: "change",
    },
  ],
});

async function submit() {
  if (await validateForm(element.value)) {
    loading.value = true;
    try {
      const resp = await axios.post("verify", form),
        data = resp.data;
      if (!data.status)
        ElNotification.error({
          title: "Verify failed",
          message: data.reason,
          showClose: false,
        });
      else {
        token.value = data.token;
        state.value = 2;
        app.exec();
        ElNotification.success({
          title: "Verify succeeded",
          message: `Welcome to Deeptrain!`,
          showClose: false,
        });
        await router.push("/");
      }
    } catch (e) {
      ElNotification.warning({
        title: "Error occurred",
        message:
          "There was an error while verifying. Please check you network and try again.",
        showClose: false,
      });
    }
    loading.value = false;
  }
}

async function resend() {
  loading.value = true;
  try {
    const resp = await axios.post("resend", form),
      data = resp.data;
    if (!data.status)
      ElNotification.error({
        title: "Resend failed",
        message: data.reason,
        showClose: false,
      });
    else
      ElNotification.success({
        title: "Resend succeeded",
        message: `We have sent a verification mail to your email address.`,
        showClose: false,
      });
  } catch (e) {
    ElNotification.warning({
      title: "Error occurred",
      message:
        "There was an error while resending. Please check you network and try again.",
      showClose: false,
    });
  }
  loading.value = false;
}
</script>

<template>
  <el-container>
    <el-header>
      <RouterLink to="/" class="header">
        <img src="/favicon.ico" alt="Deeptrain" />
      </RouterLink>
    </el-header>
    <el-main class="main">
      <h1>Verify your account</h1>
      <el-card shadow="hover" v-loading="loading">
        <div class="tips">
          We have sent a verification mail to your email address.
        </div>
        <el-form
          ref="element"
          :model="form"
          :rules="rules"
          :label-position="'top'"
        >
          <el-form-item label="Code" prop="code">
            <el-input
              v-model="form.code"
              type="text"
              minlength="6"
              maxlength="6"
            />
          </el-form-item>
          <div>
            Didn't get the email?
            <a class="resend" @click="resend">Resend Code</a>.
          </div>
          <el-alert
            class="tips"
            description="Please fill in the verification code, it will expire in 30 minutes."
            type="info"
            center
            :closable="false"
            :show-icon="false"
          ></el-alert>
          <el-button class="validate-button" @click="submit">Verify</el-button>
        </el-form>
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>
@import "@/assets/sytle/user.css";

.tips {
  text-align: center;
  max-width: 280px;
  margin: 20px 0;
}

.tips strong {
  font-weight: bolder;
}

.resend {
  cursor: pointer;
}
</style>
