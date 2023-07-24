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
      <div class="app-container">
        <a class="app" href="https://lightxi.com">
          <img src="/lightxi.png" alt="">
          <div class="desc">
            <h1>LightXi IDC</h1>
            <p>保持热爱，共赴山海</p>
          </div>
        </a>
        <a class="app" href="https://fystart.cn">
          <img src="/fystart.webp" alt="">
          <div class="desc">
            <h1>Fystart</h1>
            <p>一个简洁的起始页，为你所想</p>
          </div>
        </a>
        <a class="app" href="https://nio.fystart.cn">
          <img src="/chatnio.ico" alt="">
          <div class="desc">
            <h1>Chat Nio</h1>
            <p>AI 聊天助手</p>
          </div>
        </a>
      </div>
    </div>
  </main>
  <footer>
    <a class="copyright" href="https://www.baidu.com/baidu?ie=utf-8&wd=%E7%8F%A0%E6%B5%B7%E5%B8%82%E6%99%9E%E4%BA%91%E4%BA%91%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8" target="_blank">
      © 2023 珠海市晞云云科技有限公司
    </a>
  </footer>
</template>

<style scoped>
main {
  background: linear-gradient(rgba(10, 10, 10, .5), rgba(0, 0, 0, .5)), url("/background.webp");
  background-size: cover;
  background-position: center;
  width: 100%;
  height: 100vh;
  overflow: hidden;
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

.desc {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  user-select: none;
  white-space: nowrap;
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

.app-container {
  position: relative;
  width: 100%;
  height: max-content;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.app {
  margin: 32px;
  padding: 32px;
  width: 320px;
  height: 320px;
  backdrop-filter: blur(2px);
  background: rgba(255, 255, 255, .12);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition: .5s;
  cursor: pointer;
  color: #fff;
}

.app img {
  width: 120px;
  height: 120px;
  margin-bottom: 16px;
  user-select: none;
  background: rgb(30, 30, 30);
  border-radius: 12px;
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, .2);
}

.app h1 {
  margin-bottom: 8px;
  font-size: 24px;
  font-weight: 600;
  color: #fff;
  user-select: none;
  white-space: nowrap;
}

.app p {
  font-size: 16px;
  font-weight: 400;
  color: rgba(255, 255, 255, .75);
  user-select: none;
  white-space: nowrap;
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

footer .copyright:hover {
  color: #fff;
  background: none;
}

@media (max-width: 1200px) {
  .app {
    margin: 22px 16px;
    width: 240px;
    height: max-content;
  }

  .app img {
    width: 82px;
    height: 82px;
  }

  .app h1 {
    font-size: 20px;
  }

  .app p {
    font-size: 14px;
  }
}

@media (max-width: 800px) {
  .container .title {
    margin-top: 100px;
    font-size: 36px;
  }

  .container .subtitle {
    margin: 6px 0;
  }

  .app-container {
    flex-direction: column;
    align-items: unset;
    padding: 0 4px;
  }

  .app {
    margin: 6px 16px;
    padding: 2px;
    width: max-content;
    height: max-content;
    background: none;
    backdrop-filter: none;
    border-radius: 0;
    box-shadow: none;
    flex-direction: row;
  }

  .app .desc {
    margin-left: 16px;
    text-align: left;
    justify-content: left;
    align-items: flex-start;
  }

  .app img {
    width: 82px;
    height: 82px;
    margin: 8px 0;
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
