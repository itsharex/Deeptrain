<script setup lang="ts">

</script>
<template>
  <main>
    <header>
      <img src="/favicon.ico" alt="" class="logo">
      <div class="name">
        <span class="cn">深能科创</span>
        <span class="en">Deeptrain Team</span>
      </div>
      <div style="flex-grow: 1" />
      <div class="login">
        登录账号
      </div>
    </header>
    <div class="container">
      <div class="title">致力于更好的体验</div>
      <div class="subtitle">不为利益驱，唯献爱与梦。心中善意永存，纯粹之美在手，不断创新之路。</div>
    </div>
  </main>
  <footer>
    <span class="copyright">
      © 2023 珠海市晞云云科技有限公司 | 深能科创团队
    </span>
  </footer>
</template>

<style scoped>
main {
  background: linear-gradient(rgba(30, 30, 30, .45), rgba(0, 0, 0, .5)), url("/background.webp");
  background-size: cover;
  background-position: center;
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
  backdrop-filter: blur(18px);
  border-bottom: 1px solid rgba(255, 255, 255, .1);
  display: flex;
  flex-direction: row;
  z-index: 1;
}

.logo {
  margin: 12px 14px 12px 26px;
  width: 62px;
  height: 62px;
  user-select: none;
}

.name {
  margin: 12px 0;
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
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.container .title {
  margin-top: 160px;
  padding: 16px 18px;
  font-size: 46px;
  font-weight: 600;
  color: #fff;
  text-align: center;
  user-select: none;
  white-space: pre-wrap;
  text-shadow: 0 0 12px rgba(0, 0, 0, .6);
}

.container .subtitle {
  margin-top: 16px;
  padding: 0 24px;
  font-size: 18px;
  font-weight: 400;
  color: rgba(255, 255, 255, .75);
  text-align: center;
  user-select: none;
  white-space: pre-wrap;
  text-shadow: 0 0 12px rgba(0, 0, 0, .6);
}

footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 42px;
  padding: 1px;
  background: rgba(255, 255, 255, .12);
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, .2);
  backdrop-filter: blur(18px);
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
</style>
