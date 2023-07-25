<script setup lang="ts">
import { reactive, ref } from "vue";
import { state, username } from "@/assets/script/global";
import router from "@/router";
import axios from "axios";
import { formatDate } from "@/assets/script/time";

function logout() {
  router.push("/logout");
}

const form = reactive<Record<string, any>>({
  username: "",
  id: 0,
  email: "",
  created_at: "",
});

axios.get("info")
  .then((res) => {
    for (const key in res.data) {
      form[key] = res.data[key];
    }
    form.created_at = formatDate(form.created_at);
  })
</script>
<template>
  <el-container>
    <el-main>
      <el-card class="card">
        <div class="header">
          <div class="logo">
            <img src="/favicon.ico" alt="" />
            <span>Deeptrain 账号管理</span>
          </div>
          <div class="grow" />
          <div class="username">
            {{ username }}
          </div>
          <div class="logout" @click="logout">
            退出登录
          </div>
        </div>
      </el-card>
      <el-card class="card">
        <div class="setting">
          <div class="form general">
            <div class="title">
              <span>通用</span>
            </div>
            <div class="item">
              <div class="label">ID</div>
              <div class="grow" />
              <div class="value">{{ form.id }}</div>
            </div>
            <div class="item">
              <div class="label">用户名</div>
              <div class="grow" />
              <div class="value">{{ form.username }}</div>
            </div>
            <div class="item">
              <div class="label">邮箱</div>
              <div class="grow" />
              <div class="value">{{ form.email }}</div>
            </div>
            <div class="item">
              <div class="label">注册时间</div>
              <div class="grow" />
              <div class="value">{{ form.created_at }}</div>
            </div>
          </div>
        </div>
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>
.card {
  width: 100%;
  max-width: 820px;
  margin: 8px auto 12px;
}

.header {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.logo {
  width: max-content;
  height: max-content;
  user-select: none;
  display: flex;
  align-items: center;

}

.logo img {
  width: 36px;
  height: 36px;
}

.logo span {
  font-size: 24px;
  font-weight: 600;
  margin-left: 16px;
  color: rgba(255, 255, 255, 0.9);
}

.username {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin-right: 16px;
  user-select: none;
  white-space: nowrap;
}

.logout {
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.2);
  padding: 8px 16px;
  border-radius: 4px;
  transition: .5s;
  user-select: none;
  white-space: nowrap;
}

.logout:hover {
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.setting {
  display: flex;
  width: 100%;
  flex-direction: row;
  align-items: flex-start;
}

.form {
  width: 100%;
  margin: 0 16px;
}

.form .title {
  margin-bottom: 16px;
}

.form .title span {
  font-size: 24px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  user-select: none;
}

.form .title:before {
  content: "";
  display: inline-block;
  top: 4px;
  left: -2px;
  width: 4px;
  height: 24px;
  background: #409eff;
  margin-right: 8px;
  border-radius: 2px;
  user-select: none;
}

.form .item {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 16px;
}

.form .item .label {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin-right: 16px;
  width: 100px;
  user-select: none;
  white-space: nowrap;
}

.form .item .value {
  font-size: 16px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.75);
  user-select: none;
  white-space: nowrap;
}

@media (max-width: 620px) {
  .logo span {
    display: none;
  }
}
</style>
