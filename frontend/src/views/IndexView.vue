<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import axios from "axios";
import { RouterLink } from "vue-router";
import { state } from "@/assets/script/global";
import Translate from "@/components/icons/translate.vue";
import Home from "@/components/icons/home.vue";
import Login from "@/components/icons/login.vue";
import Setting from "@/components/icons/setting.vue";

const I18nPopover = ref(null);

const currentIcon = ref<HTMLElement | null>(null);
function iconToggle(e: Event) {
  let target = e.target as HTMLElement;
  const name = target.localName;
  if (name === "path") target = target.parentElement as HTMLElement;
  if (name === "a") target = target.children[0] as HTMLElement;
  target.classList.add("checked");
  console.log(currentIcon.value)
  if (currentIcon.value) currentIcon.value.classList.remove("checked");
}
</script>
<template>
  <header class="nav">
    <router-link class="logo no-background" to="/">
      <img src="/favicon.ico" alt="" />
      <h2>Deeptrain</h2>
    </router-link>
    <div class="flex" />

    <div class="translate" v-popover="I18nPopover">
      <translate class="icon" />
    </div>
    <el-popover ref="I18nPopover" trigger="click" virtual-triggering persistent>
      <span>Hi</span>
    </el-popover>

    <img class="avatar" v-if="state === 2" src="/user.png" alt="" />
    <router-link class="no-background" to="/login" v-else>
      <el-button class="nav-btn" type="primary">Login</el-button>
    </router-link>
  </header>
  <aside class="sidebar">
    <router-link @click="iconToggle" class="no-background" to="/"><home class="icon checked" ref="currentIcon" /></router-link>
    <router-link @click="iconToggle" class="no-background" to="/settings"><setting class="icon" /></router-link>
    <div class="flex" />
    <router-link class="no-background" to="/login" v-if="state !== 2">
      <el-button class="nav-btn" type="primary">
        <login class="icon" />
      </el-button>
    </router-link>
  </aside>
</template>

<style scoped>
@import "@/assets/sytle/index.css";
</style>
