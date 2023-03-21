<div align="center">

# <a href="https://deeptrain.net"><img height='44px' width='44px' src='favicon.ico' style="transform: translateY(10px)"></img> <span>Deeptrain<span></a>
###  🔥 An Open Source Deep Reinforcement Learning training platform
###  🔥 一个开源深度强化学习训练平台
</div>

---
<div align="center">

[![Deeptrain Github Stats](https://stats.deeptrain.net/repo/zmh-program/Deeptrain?theme=dark)](https://github.com/zmh-program/code-statistic)

![system: linux/unix](https://img.shields.io/badge/system-Unix-important)
&nbsp;
![python: 3.9](https://img.shields.io/badge/python-3.9-success)
&nbsp;
![django: 4.1](https://img.shields.io/badge/Django-4.1-informational)
&nbsp;
![vue: 3.2](https://img.shields.io/badge/vue-3.2-42b883)

</div>

---


## 🚀️ ScreenShot 🎋

![screenshot](/docs/screenshot/screenshot.png)

## 🌊 Website Features 🔮

1. [X]  🍹  **User**
2. [X]  🥁  **Files**
3. [X]  🧃  **Websocket protocol & Instant Message**
4. [X]  🍵  **Website Management (GeoIP, Monitor)**
5. [X]  ☕  **Database & Cache**
6. [X]  🍷  **Embedding Applications**
7. [X]  👋  **OAuth** *(Open Authorization)*
8. [X]  📚  **Blog & Text Audit**
9. [X]  🔍  **IP Verify**
10. [ ] 🌀  **Front-end and Back-end Separation**
11. [ ] 🌏  **i18n** *(Internationalization)*
12. [ ] 📫  **Email Validation**

## ✨ Open Authorization Support 🎈

<div align="center">

[<img height="56px" src="https://cdn-icons-png.flaticon.com/128/919/919847.png" alt="github">](https://github.com/)&nbsp;
[<img height="56px" src="https://gitee.com/favicon.ico" alt="gitee">](https://gitee.com/)&nbsp;

</div>
<br>

## 🏠 Embedding Applications Structure 🎫

![application](/docs/screenshot/application.jpg)

### [👉 Production & Deployment 👈](/docs/RUN.md)

## 📜 Change Log 📰

### 🔨 version `1.x.x`

- 🥎 `Release 1.0`

1. Basic User Features (login, logout, register, cookies validate)

- 🌿 `Pre 1.1`
  1. Prepare to migrate `channels` to `dwebsocket` (websocket protocol)
<br><br>
- 🎍 `Pre 1.2`
  1. Update Static Files

### 🛠 version `2.x.x`

- 🍒 `Release 2.0.0`
  1. 🎉 Emoji Support 🎉
  2. 📕 iframe Support ( home page)📘
  3. ✈ beautify login / register page ✈
  4. 🔥 Websocket: Channels -> dwebsocket 🔥
  5. 🚀 Application Config 🚀
<br><br>
- 🍎 `Release 2.1.0 to 2.1.3`
  1. **putting on `ICP record`, deploy website**
  2. Use Django-form
  3. Add `django-simple-captcha` validation
  4. Add Embedding Application Repository Information(`shields.io`)
  5. Add `Gunicorn` Support
  6. Add `Websocket Security`(wss) Support
<br><br>
- 🍋 `Release 2.2.0 to 2.2.4.1`
  - File Features
    1. validation, limits (including `permission`, `file size`, `file name length`)
    2. download
    3. upload (client `ajax` upload, server `uuid` file handle)
    4. cache
    5. pagination
<br><br>
- 🎁 `Pre 2.3.0 to 2.3.1`
  - GeoIP Monitor (User country, request region analysis) v2.3.0-2.3.1
<br><br>
- 🎯 `Pre 2.3.2-alpha to 2.3.2-beta.2`
  - Instant Message (Websocket Protocol)
<br><br>
- 🌍 `Pre 2.4.0 to 2.4.1`
  - `django-simple-captcha` -> `hCaptcha` verify
<br><br>
- ✈ `Pre 2.5.0 to 2.5.0.2`
  - Improve the performance of code & database
  - User Django-auth
<br><br>
- 🌲 `Pre 2.6.0 to 2.6.0.3`
  - Replit and Vercel deployment
<br><br>
- 🔥 `Pre 2.7.0 to 2.7.2.3`
  - Admin Analysis Pages
    - Users & Requests Region Distribution
    - Server & Website Monitor
<br><br>
- 🎇 `Release 2.7.3 to 2.7.12`
  - Change Password Page
  - **Intelligent verification**
    - change password page
    - login page
    - register page
  - User Avatars
  - update Profile Page (`gitee`, `github`, `codepen` info)
<br><br>
- 🍀 `Pre 2.8.0 to 2.8.4.2`
  - dockerfile
  - update `Embedding Applications` structure
  - `SiteApplication` construction
<br><br>
- 📕 `Pre 2.9.0 to 2.9.1`
  - Reduce Photo size (per < 0.6MiB)
<br><br>
- 🚀 `Release 2.10.0 to 2.10.3`
  - `hCaptcha` -> `Cloudflare Turnstile` verify
  - Network attack and defense TEST (php) **Thanks to @APGPerson**
    - fixed file download bug
<br><br>
- 📕 `Pre 2.11.0 to 2.11.6`
  - Update README style
<br><br>
- 🙌 `Pre 2.12.0 to 2.12.6.2`
  - update models
  - update im
  - Use Verify using `Turnstile` and `hCaptcha` dual components
    - `Turnstile`: file-upload, login, change-password pages
    - `hCaptcha`: register page
  - Fixed the failure of multiple verification codes submitted by the deployment environment
    - call `(hcaptcha or turnstile).refresh()`
<br><br>
- 🧃 `Release 2.13.0 to 2.13.3`
  - **OAuth** *(Open Authorization)*
    - OAuth Login
    - OAuth Bind *(Support `Github`, `Gitee`)*
    - OAuth Config
<br><br>
- 📚 `Release 2.14.0-alpha to 2.14.7.1`
  - **Markdown Blog System** (`haystack` & `whoosh` & `jieba` & `mptt` & `layui`)
    - Articles
    - Comments (two-level)
    - Tags
    - Likes
    - Search & Highlight (haystack)
<br><br>
- ⛳ `Pre 2.15.0 to 2.15.5`
  - change code & frontend structure
  - django commands
  - operation throttle
<br><br>
- 🔍 `Pre 2.16.0 to 2.16.4.4`
  - Text Audit (paddlehub dataset & model)
  - Docker-compose
<br><br>
- 👆 `Release 2.17 to 2.17.0.3`
  - python 3.7 -> 3.9
  - django 3.2 -> 4.1

### ⚡ version `3.x.x`
- Zh-Website -> Deeptrain
- Vue3 + Django REST
- MAIL

## Thanks

<div align="center">


[<img height="32px" src="https://www.kaggle.com/static/images/favicon.ico" alt="kaggle">](https://kaggle.com/)&nbsp;
[<img height="32px" src="https://docs.replit.com/image/logo.svg" alt="replit">](https://replit.com/)&nbsp;
[<img height="32px" src="https://cdn-icons-png.flaticon.com/128/5969/5969044.png" alt="cloudflare">](https://cloudflare.com/)&nbsp;
[<svg viewBox="0 0 32 32" style="width: 32px; height: 32px; fill:orange"><g><path d="M4.54,9.46,2.19,7.1a6.93,6.93,0,0,0,0,9.79l2.36-2.36A3.59,3.59,0,0,1,4.54,9.46Z" style="fill:var(--colab-logo-dark)"></path><path d="M2.19,7.1,4.54,9.46a3.59,3.59,0,0,1,5.08,0l1.71-2.93h0l-.1-.08h0A6.93,6.93,0,0,0,2.19,7.1Z" style="fill:var(--colab-logo-light)"></path><path d="M11.34,17.46h0L9.62,14.54a3.59,3.59,0,0,1-5.08,0L2.19,16.9a6.93,6.93,0,0,0,9,.65l.11-.09" style="fill:var(--colab-logo-light)"></path><path d="M12,7.1a6.93,6.93,0,0,0,0,9.79l2.36-2.36a3.59,3.59,0,1,1,5.08-5.08L21.81,7.1A6.93,6.93,0,0,0,12,7.1Z" style="fill:var(--colab-logo-light)"></path><path d="M21.81,7.1,19.46,9.46a3.59,3.59,0,0,1-5.08,5.08L12,16.9A6.93,6.93,0,0,0,21.81,7.1Z" style="fill:var(--colab-logo-dark)"></path></g></svg>](https://colab.research.google.com)
<br>
[<img height="72px" src="https://www.rainyun.cc/img/logo.3dcf7adc.png" alt="rainyun" style="background: #fff; border-radius:6px;padding: 8px 12px; margin-top:4px">](https://www.rainyun.cc/?ref=MzE4MDA=)

</div>
