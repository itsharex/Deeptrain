<script setup lang="ts">
import { ref } from "vue";
import { state, username } from "@/assets/script/global";
import router from "@/router";

function logout() {
  router.push("/logout");
}
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
    </el-main>
  </el-container>
</template>

<style scoped>
.card {
  width: 100%;
  max-width: 820px;
  margin: 0 auto;
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
}

.logout:hover {
  border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>
