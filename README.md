<div align="center">

# <a href="https://deeptrain.net"><img height='44px' width='44px' src='favicon.ico' style="transform: translateY(10px)"></img></a> <a href="https://deeptrain.net"><span>Deeptrain<span></a>
###  🔥 An Open Source Deep Reinforcement Learning training platform X Unified Account Management System
###  🔥 一个开源深度强化学习训练平台 X 统一账号管理
</div>

---
<div align="center">

[![Deeptrain Github Stats](https://stats.deeptrain.net/repo/zmh-program/Deeptrain?theme=dark)](https://github.com/zmh-program/code-statistic)

![system: linux/unix](https://img.shields.io/badge/system-Unix-important)
&nbsp;
![python: 3.9](https://img.shields.io/badge/python-3.9-success)
&nbsp;
![go: 1.22](https://img.shields.io/badge/go-1.22-00ADD8)
&nbsp;
![django: 4.1](https://img.shields.io/badge/Django-4.1-informational)
&nbsp;
![vue: 3.2](https://img.shields.io/badge/vue-3.2-42b883)
&nbsp;
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fzmh-program%2FDeeptrain.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fzmh-program%2FDeeptrain?ref=badge_shield)

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
10. [x] 🌀  **Front-end and Back-end Separation**
11. [x] 🌏  **i18n** *(Internationalization)*
12. [x] 📫  **Email Validation**
13. [x] 📧  **Notification**
14. [x] 📝  **UAM**

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
- Golang + Vue


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fzmh-program%2FDeeptrain.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fzmh-program%2FDeeptrain?ref=badge_large)
