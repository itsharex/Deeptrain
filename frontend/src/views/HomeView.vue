<script setup lang="ts">
import { ref } from "vue";
import { RouterLink } from "vue-router";
import { state } from "@/assets/script/global";
</script>
<template>
  <el-container>
    <el-main>
      <el-card class="card">
        <div class="logo">
          <img src="/favicon.ico" alt="" />
          <span>Deeptrain 账号管理</span>
        </div>
        <div class="grow" />
        <div class="logout">
          退出登录
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
</style>
