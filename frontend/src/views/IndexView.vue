<script setup lang="ts">
import router from "@/router";
import { useI18n } from "vue-i18n";
import World from "@/components/icons/world.vue";
import Github from "@/components/icons/github.vue";
import { language } from "@/config";

const { t, locale } = useI18n();
locale.value = language.value;

function login() {
  router.push("/login");
}

function toggleI18n() {
  if (locale.value === "en") {
    locale.value = "zh";
  } else {
    locale.value = "en";
  }
  language.value = locale.value;
}
</script>
<template>
  <main>
    <header :class="{ chinese: locale === 'zh' }">
      <img src="/favicon.ico" alt="" class="logo" />
      <div class="name">
        <span class="cn">{{ t("title") }}</span>
        <span class="en">Deeptrain Team</span>
      </div>
      <div style="flex-grow: 1" />
      <div class="i18n" @click="toggleI18n"><world /></div>
      <div class="login" @click="login">{{ t("login") }}</div>
    </header>
    <div class="container">
      <div class="landing">
        <img
          src="https://cdn.zmh-program.site/deeptrain/background.jpg"
          alt=""
          class="background"
          loading="lazy"
        />
        <div class="left">
          <div class="top">{{ t("title") }}</div>
          <div class="title">{{ t("subtitle") }}</div>
          <div class="subtitle">{{ t("slogan") }}</div>
        </div>
      </div>
      <div class="circle" />
      <section class="product">
        <div class="line">
          <span>{{ t("product") }}</span>
          <p>Our Products</p>
        </div>
        <div class="app-container">
          <a class="app" href="https://lightxi.com">
            <img src="/lightxi.png" alt="" />
            <div class="desc">
              <h1>LightXi Cloud</h1>
              <p>{{ t("lightxi-cloud") }}</p>
            </div>
          </a>
          <a class="app" href="https://fystart.cn">
            <img src="/fystart.webp" alt="" />
            <div class="desc">
              <h1>Fystart</h1>
              <p>{{ t("fystart") }}</p>
            </div>
          </a>
          <a class="app" href="https://notes.lightxi.com">
            <img src="/lightnotes.ico" alt="" />
            <div class="desc">
              <h1>Light Notes</h1>
              <p>{{ t("lightnotes") }}</p>
            </div>
          </a>
          <a class="app" href="https://nio.fystart.cn">
            <img src="/chatnio.png" alt="" />
            <div class="desc">
              <h1>Chat Nio</h1>
              <p>{{ t("chatnio") }}</p>
            </div>
          </a>
        </div>
      </section>
      <section class="team">
        <div class="line">
          <span>{{ t("team") }}</span>
          <p>Our Team</p>
          <div class="app-container">
            <a class="app" href="https://zmh-program.site">
              <img
                src="https://zmh-program.site/avatar/zmh-program.webp"
                alt=""
              />
              <div class="desc">
                <h1>zmh-program</h1>
                <p>— {{ t("motto-zmh") }}</p>
                <a
                  href="https://github.com/zmh-program"
                  target="_blank"
                  class="github"
                >
                  <github />
                </a>
              </div>
            </a>
            <a class="app" href="https://shinezz.cc">
              <img src="https://zmh-program.site/friend/sh1n3zz.webp" alt="" />
              <div class="desc">
                <h1>Sh1n3zZ</h1>
                <p>— {{ t("motto-zz") }}</p>
                <a
                  href="https://github.com/sh1n3zz"
                  target="_blank"
                  class="github"
                >
                  <github />
                </a>
              </div>
            </a>
          </div>
        </div>
      </section>
    </div>
    <footer>
      <a href="https://lightxi.com" style="padding: 2px 0" target="_blank">
        © 2023 {{ t("copyright") }}
      </a>
      <div class="nav">
        <router-link to="/service" style="transform: translateY(2px)">{{
          t("service")
        }}</router-link>
        <div class="split">|</div>
        <router-link to="/privacy" style="transform: translateY(1px)">{{
          t("privacy")
        }}</router-link>
      </div>
      <div class="gov">
        <a href="https://beian.miit.gov.cn/" target="_blank">
          <img
            src="https://lightxi.com/themes/web/mfQloud/assets/images/gov.webp"
            alt=""
          />
          粤ICP备2023066011号-1
        </a>
      </div>
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
    "service": "Terms of Service",
    "privacy": "Privacy Policy",
    "copyright": "LightXi Inc.",
    "product": "",
    "team": "",
    "lightxi-cloud": "Stay passionate and explore mountains and seas together.",
    "fystart": "A simple start page, crafting efficient tools, tailored to your needs.",
    "lightnotes": "Keep small and large matters to heart. A lightweight note app that supports multiple file formats and parsing.",
    "chatnio": "A simple, elegant, lightweight open-source AI chat assistant.",
    "motto-zmh": "Nothing is impossible.",
    "motto-zz": "There is no justice in following unjust laws."
  },
  "zh": {
    "title": "深能科创",
    "subtitle": "致力于更好的体验",
    "slogan": "保持热爱，共赴山海。",
    "login": "登录账号",
    "copyright": "晞云",
    "service": "服务条款",
    "privacy": "隐私政策",
    "product": "我们的产品",
    "team": "开源团队",
    "lightxi-cloud": "晞云云计算 - 保持热爱，共赴山海。",
    "fystart": "一个简洁的起始页，铸就高效率工具，为你所想。",
    "lightnotes": "大小事，随手记。一个极简、美观、多端同步、支持解析多种文件的轻量化在线便签。",
    "chatnio": "一个简洁、美观、轻量的开源 AI 聊天助手。",
    "motto-zmh": "Nothing is impossible.",
    "motto-zz": "There is no justice in following unjust laws."
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
  background: rgba(255, 255, 255, 0.12);
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(18px) blur(18px) saturate(50%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
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
  font-family: Helvetica, PingFang SC, Microsoft YaHei, sans-serif;
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
  background: rgba(255, 255, 255, 0.12);
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: 0.5s;
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.2);
  color: rgba(255, 255, 255, 0.8);
  white-space: nowrap;
}

.login:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.2);
}

.i18n {
  margin: 16px 12px 16px 0;
  display: flex;
  flex-direction: row;
  align-items: center;
  user-select: none;
  background: rgba(255, 255, 255, 0.12);
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: 0.5s;
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.2);
  fill: rgba(255, 255, 255, 0.8);
  white-space: nowrap;
}

.i18n:hover {
  fill: #fff;
  background: rgba(255, 255, 255, 0.2);
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
}

.landing .background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  user-select: none;
  object-fit: cover;
  object-position: center;
}

section {
  width: 100%;
  height: max-content;
}

.team {
  background: #181717;
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
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.2);
}

.gov img {
  width: 14px;
  height: 14px;
  margin: 2px;
  transform: translateY(4px);
  transition: 0.25s;
  opacity: 0.8;
}

.gov:hover img {
  opacity: 1;
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
  text-shadow: 0 0 12px rgba(0, 0, 0, 0.6);
  animation: LandingAnimation 1s forwards;
}

.landing .top {
  padding: 16px 18px 0;
  font-size: 32px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  user-select: none;
  white-space: pre-wrap;
  text-shadow: 0 0 12px rgba(0, 0, 0, 0.6);
  transform: translateY(12px);
}

.landing .title {
  padding: 16px 18px;
  font-size: 46px;
  font-weight: 600;
  color: #fff;
  user-select: none;
  white-space: pre-wrap;
  text-shadow: 0 0 12px rgba(0, 0, 0, 0.6);
}

.landing .subtitle {
  margin-top: 16px;
  padding: 0 24px;
  font-size: 18px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.75);
  user-select: none;
  white-space: pre-wrap;
  text-shadow: 0 0 12px rgba(0, 0, 0, 0.6);
}

.line {
  margin: 64px 0 32px;
  padding: 0 24px;
  font-size: 24px;
  font-weight: 600;
  color: #fff;
  user-select: none;
  white-space: pre-wrap;
  text-shadow: 0 0 12px rgba(0, 0, 0, 0.6);
  text-align: center;
}

section.white .line {
  color: #1e1e20;
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.6);
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
  font-family: Helvetica, Arial, sans-serif, "Apple Color Emoji",
    "Segoe UI Emoji", "Segoe UI Symbol";
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
  transition: 0.5s;
  cursor: pointer;
  color: #fff;
}

.app:hover {
  border: 1px solid #252529;
  background: #232325;
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.2);
}

.app img {
  width: 58px;
  height: 58px;
  background: #1e1e20;
  padding: 4px;
  margin-bottom: 16px;
  user-select: none;
  border-radius: 12px;
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.5s;
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
  transition: 0.5s;
}

.app:hover .desc {
  margin-top: 4px;
}

.app h1 {
  margin-bottom: 14px;
  line-height: 24px;
  font-size: 22px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.86);
  user-select: none;
  white-space: nowrap;
  font-family: "JetBrains Mono", monospace;
}

.app p {
  font-size: 16px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.75);
  user-select: none;
  white-space: pre-wrap;
}

.team img {
  background: none;
}

.team .desc {
  min-height: 120px;
}

.team .github {
  margin-top: auto;
  margin-left: auto;
  transform: translate(8px, 2px);
  width: 24px;
  height: 24px;
  fill: rgba(255, 255, 255, 0.75);
  transition: 0.5s;
  background: none;
}

footer {
  width: 100%;
  height: max-content;
  padding: 24px 8px;
  gap: 4px;
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.2);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  justify-content: center;
  align-items: center;
  display: flex;
  flex-direction: column;
  z-index: 1;
}

.nav {
  display: flex;
  flex-direction: row;
  align-items: center;
  user-select: none;
}

.split {
  content: "|";
  margin: 0 4px;
  user-select: none;
  color: rgba(255, 255, 255, 0.5);
}

footer a {
  font-size: 14px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.75);
  user-select: none;
  white-space: nowrap;
  text-shadow: 0 0 12px rgba(0, 0, 0, 0.6);
}

footer a:hover {
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

  .container .top {
    font-size: 22px;
  }
}

@media (max-width: 400px) {
  .landing .left {
    padding: 0 12px;
  }

  .container .title {
    font-size: 22px;
  }

  .container .top {
    font-size: 18px;
  }

  .name .cn {
    font-size: 18px;
    white-space: pre-wrap;
  }

  .name {
    display: flex;
    justify-content: center;
  }

  .chinese .name .cn {
    white-space: nowrap;
  }

  .name .en {
    display: none;
  }
}
</style>
