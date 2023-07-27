<script setup lang="ts">
import router from "@/router";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

function login() {
  router.push("/login");
}
</script>
<template>
  <main>
    <header>
      <img src="/favicon.ico" alt="" class="logo">
      <div class="name">
        <span class="cn">{{ t('title') }}</span>
        <span class="en">Deeptrain Team</span>
      </div>
      <div style="flex-grow: 1" />
      <div class="login" @click="login">{{ t('login') }}</div>
    </header>
    <div class="container">
      <div class="landing">
        <div class="left">
          <div class="top">{{ t('title') }}</div>
          <div class="title">{{ t('subtitle') }}</div>
          <div class="subtitle">{{ t('slogan') }}</div>
        </div>
      </div>
      <div class="circle" />
      <div class="line">
        <span>{{ t('product') }}</span>
        <p>Our Products</p>
      </div>
      <div class="app-container">
        <a class="app" href="https://lightxi.com">
          <img src="/lightxi.png" alt="">
          <div class="desc">
            <h1>LightXi Cloud</h1>
            <p>{{ t('lightxi-cloud') }}</p>
          </div>
        </a>
        <a class="app" href="https://fystart.cn">
          <img src="/fystart.webp" alt="">
          <div class="desc">
            <h1>Fystart</h1>
            <p>{{ t('fystart') }}</p>
          </div>
        </a>
        <a class="app" href="https://notes.lightxi.com">
          <img src="/lightnotes.ico" alt="">
          <div class="desc">
            <h1>Light Notes</h1>
            <p>{{ t('lightnotes') }}</p>
          </div>
        </a>
        <a class="app" href="https://nio.fystart.cn">
          <img src="/chatnio.png" alt="">
          <div class="desc">
            <h1>Chat Nio</h1>
            <p>{{ t('chatnio') }}</p>
          </div>
        </a>
      </div>
    </div>
    <footer>
      <a class="copyright" href="https://www.baidu.com/baidu?ie=utf-8&wd=%E7%8F%A0%E6%B5%B7%E5%B8%82%E6%99%9E%E4%BA%91%E4%BA%91%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8" target="_blank">
        © 2023 {{ t('copyright') }}
      </a>
    </footer>
  </main>
</template>
<i18n>
{
  "en": {
    "title": "DeepTech Innovation",
    "subtitle": "Committed to a better experience",
    "slogan": "Stay passionate and explore mountains and seas together.",
    "login": "Login",
    "copyright": "Lightxi Cloud Technology Ltd.",
    "product": "",
    "lightxi-cloud": "Stay passionate and explore mountains and seas together.",
    "fystart": "A simple start page, crafting efficient tools, tailored to your needs.",
    "lightnotes": "Keep small and large matters to heart. A lightweight note app that supports multiple file formats and parsing.",
    "chatnio": "A simple, elegant, lightweight open-source AI chat assistant."
  },
  "zh": {
    "title": "深能科创",
    "subtitle": "致力于更好的体验",
    "slogan": "保持热爱，共赴山海。",
    "login": "登录账号",
    "copyright": "珠海市晞云云科技有限公司",
    "product": "我们的产品",
    "lightxi-cloud": "晞云云计算 - 保持热爱，共赴山海。",
    "fystart": "一个简洁的起始页，铸就高效率工具，为你所想。",
    "lightnotes": "大小事，随手记。一个极简、美观、多端同步、支持解析多种文件的轻量化在线便签。",
    "chatnio": "一个简洁、美观、轻量的开源 AI 聊天助手。"
  }
}
</i18n>
<style scoped>
@import "@/assets/style/anim.css";
main {
  background: #1e1e20;
  background-size: cover;
  width: 100%;
  height: 100vh;
}

header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 84px;
  padding: 1px;
  background: rgba(255, 255, 255, .12);
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, .2);
  backdrop-filter: blur(18px) blur(18px) saturate(50%);
  border-bottom: 1px solid rgba(255, 255, 255, .1);
  display: flex;
  flex-direction: row;
  z-index: 1;
  animation: FadeInAnimation 1s;
}

.logo {
  margin: 12px 14px 12px 26px;
  width: 62px;
  height: 62px;
  user-select: none;
}

.name {
  margin: 13px 0;
  font-size: 20px;
  font-weight: 600;
  color: #fff;
  display: flex;
  flex-direction: column;
  flex: 1;
  user-select: none;
  white-space: nowrap;
}

.name .cn {
  font-family: Helvetica,PingFang SC,Microsoft YaHei,sans-serif;
  font-weight: 600;
}

.name .en {
  font-size: 16px;
  font-weight: 400;
  color: #fff;
  transform: translateY(-2px);
}

.login {
  margin: 16px 26px 16px 0;
  display: flex;
  flex-direction: row;
  align-items: center;
  user-select: none;
  background: rgba(255, 255, 255, .12);
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: .5s;
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, .2);
  color: rgba(255, 255, 255, .8);
  white-space: nowrap;
}

.login:hover {
  color: #fff;
  background: rgba(255, 255, 255, .2);
}

.container {
  position: relative;
  background: #1e1e20;
  width: 100%;
  height: max-content;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-x: hidden;
}

.landing {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: row;
  align-items: center;
  background: linear-gradient(to right, rgba(0, 0, 0, .2), rgba(10, 10, 10, .05)), url(/background.png);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.circle {
  position: absolute;
  top: calc(100vh - 16px);
  left: 50%;
  width: 32px;
  height: 32px;
  transform: translateX(-50%);
  border-radius: 50%;
  background: #1e1e20;
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, .2);
}

@keyframes LandingAnimation {
  0% {
    transform: translateX(-100px);
    opacity: 0;
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}

.landing .left {
  margin-left: 160px;
  padding: 16px 18px;
  font-size: 46px;
  font-weight: 600;
  color: #fff;
  text-align: left;
  user-select: none;
  white-space: pre-wrap;
  text-shadow: 0 0 12px rgba(0, 0, 0, .6);
  animation: LandingAnimation 1s forwards;
}

.landing .top {
  padding: 16px 18px 0;
  font-size: 32px;
  font-weight: 600;
  color: rgba(255, 255, 255, .95);
  user-select: none;
  white-space: pre-wrap;
  text-shadow: 0 0 12px rgba(0, 0, 0, .6);
  transform: translateY(12px);
}

.landing .title {
  padding: 16px 18px;
  font-size: 46px;
  font-weight: 600;
  color: #fff;
  user-select: none;
  white-space: pre-wrap;
  text-shadow: 0 0 12px rgba(0, 0, 0, .6);
}

.landing .subtitle {
  margin-top: 16px;
  padding: 0 24px;
  font-size: 18px;
  font-weight: 400;
  color: rgba(255, 255, 255, .75);
  user-select: none;
  white-space: pre-wrap;
  text-shadow: 0 0 12px rgba(0, 0, 0, .6);
}

.line {
  margin: 64px 0 32px;
  padding: 0 24px;
  font-size: 24px;
  font-weight: 600;
  color: #fff;
  user-select: none;
  white-space: pre-wrap;
  text-shadow: 0 0 12px rgba(0, 0, 0, .6);
  text-align: center;
}

.line:before {
  content: "";
  position: absolute;
  top: -16px;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 4px;
  background: #3370ff;
  border-radius: 100px;
}

.line span {
  font-family: Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';
}

.app-container {
  position: relative;
  width: 100%;
  height: max-content;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  margin-bottom: 64px;
}

.app {
  margin: 32px;
  padding: 32px;
  width: 320px;
  height: max-content;
  min-height: 268px;
  border: 1px solid #252529;
  border-radius: 12px;
  background: #252529;
  display: flex;
  flex-direction: column;
  transition: .5s;
  cursor: pointer;
  color: #fff;
}

.app:hover {
  border: 1px solid #252529;
  background: #232325;
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, .2);
}

.app img {
  width: 58px;
  height: 58px;
  background: #1e1e20;
  padding: 4px;
  margin-bottom: 16px;
  user-select: none;
  border-radius: 12px;
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, .2);
  transition: .5s;
}

.app:hover img {
  width: 66px;
  height: 66px;
}

.app .desc {
  display: flex;
  margin-top: 12px;
  flex-direction: column;
  text-align: left;
  user-select: none;
  white-space: nowrap;
  transition: .5s;
}

.app:hover .desc {
  margin-top: 4px;
}

.app h1 {
  margin-bottom: 14px;
  line-height: 24px;
  font-size: 22px;
  font-weight: 600;
  color: rgba(255,255,255,.86);
  user-select: none;
  white-space: nowrap;
  font-family: "JetBrains Mono", monospace;
}

.app p {
  font-size: 16px;
  font-weight: 400;
  color: rgba(255, 255, 255, .75);
  user-select: none;
  white-space: pre-wrap;
}

footer {
  width: 100%;
  height: 42px;
  padding: 1px;
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, .2);
  border-top: 1px solid rgba(255, 255, 255, .1);
  justify-content: center;
  align-items: center;
  display: flex;
  flex-direction: row;
  z-index: 1;
}

footer .copyright {
  font-size: 14px;
  font-weight: 400;
  color: rgba(255, 255, 255, .75);
  user-select: none;
  white-space: nowrap;
  text-shadow: 0 0 12px rgba(0, 0, 0, .6);
}

footer .copyright:hover {
  color: #fff;
  background: none;
}

@media (max-width: 800px) {
  .landing .left {
    margin-left: 0;
    padding: 0 16px;
  }
}

@media (max-width: 520px) {
  .logo {
    display: none;
  }

  .name {
    margin-left: 16px;
  }

  .container .title {
    font-size: 26px;
  }
}
</style>
