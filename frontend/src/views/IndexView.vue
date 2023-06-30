<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import { RouterLink } from "vue-router";
import { state } from "@/assets/script/global";
import Translate from "@/components/icons/translate.vue";
import Home from "@/components/icons/home.vue";
import Login from "@/components/icons/login.vue";

const I18nPopover = ref(null);
</script>
<template>
  <header class="nav">
    <router-link class="logo no-background" to="/">
      <img src="/favicon.ico" alt="" />
      <h2>Deeptrain</h2>
    </router-link>
    <div class="flex" />

    <el-button type="text" plain class="translate" v-popover="I18nPopover">
      <translate class="icon" />
    </el-button>
    <el-popover ref="I18nPopover" trigger="click" virtual-triggering persistent>
      <span>Hi</span>
    </el-popover>

    <img class="avatar" v-if="state === 2" src="/user.png" alt="" />
    <router-link class="no-background" to="/login" v-else>
      <el-button class="nav-btn" type="primary">登录</el-button>
    </router-link>
  </header>
  <aside class="sidebar">
    <router-link class="no-background" to="/">
      <home class="icon" />
    </router-link>
    <div class="flex" />
    <router-link class="no-background" to="/login">
      <el-button class="nav-btn" type="primary">
        <login class="icon" />
      </el-button>
    </router-link>
  </aside>
</template>

<style scoped>
@import "@/assets/sytle/index.css";
</style>
