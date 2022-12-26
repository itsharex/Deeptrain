# Zh Website

![GitHub forks](https://img.shields.io/github/forks/zmh-program/Zh-Website)
![GitHub Repo stars](https://img.shields.io/github/stars/zmh-program/Zh-Website)
![GitHub repo size](https://img.shields.io/github/repo-size/zmh-program/Zh-Website)
![GitHub repo file count](https://img.shields.io/github/directory-file-count/zmh-program/Zh-Website)
![GitHub](https://img.shields.io/github/license/zmh-program/Zh-Website)

[![star](https://gitee.com/zmh-program/Zh-Website/badge/star.svg?theme=dark)](https://gitee.com/zmh-program/Zh-Website/stargazers)
[![fork](https://gitee.com/zmh-program/Zh-Website/badge/fork.svg?theme=dark)](https://gitee.com/zmh-program/Zh-Website/members)

> 🔥 Django WSGI Website, embedding applications in the website.

> **Website (`LightHouse`)**
> 1. **[zmh-program.site](https://zmh-program.site) - tencent cloud**
> 2. *[zh-website.zmh-program.repl.co](https://zh-website.zmh-program.repl.co) - replit*
> 3. *[zh-website.vercel.app](https://zh-website.vercel.app) - vercel (redirect)*

## 🚀️ ScreenShot

![screenshot](/screenshot/screenshot.png)

## 🍉 QuickStart

- `MySQL` `localhost:3306`

  > DjangoWebsite / settings.py / line:94
  >
- `Redis` `127.0.0.1:6379`

  > DjangoWebsite / settings.py / line:107 & line:83
  >
- `Unix/Linux system`
- `python 3.7+`

  *(run in the parent directory)*

> mysql
>
> ```sql
> create DATABASE `django-database`;
> ```

> command line
>
> ```commandline
> cd Zh-Website
> pip install -r requirements.txt
>
> python manage.py makemigrations
> python manage.py migrate
>
> python manage.py collectstatic
> ```

## 🌊 Website Features

1. **User**
2. **Files**
3. **Websocket protocol & Instant Message**
4. **Website Management**
5. **Database & Cache**
6. **Embedding Applications**

## 🏠 Embedding Applications Structure

![application](/screenshot/application.jpg)

## 📜 Change Log

### version `1.x.x`

- 🥎 `Release 1.0`
 1. Basic User Features (login, logout, register, cookies validate)
- 🌿 `Pre 1.1`
  1. Prepare to migrate `channels` to `dwebsocket` (websocket protocol)
- 🎍 `Pre 1.2`
  1. Update Static Files

### version `2.x.x`
- 🍒 `Release 2.0.0`
  1. 🎉 Emoji Support 🎉
  2. 📕 iframe Support ( home page)📘
  3. ✈ beautify login / register page ✈
  4. 🔥 Websocket: Channels -> dwebsocket 🔥
  5. 🚀 Application Config 🚀
- 🍎 `Release 2.1.3`
  1. **putting on `ICP record`, deploy website**
  2. Use Django-form
  3. Add `django-simple-captcha` validation
  4. Add Embedding Application Repository Information(`shields.io`)
  5. Add `Gunicorn` Support
  6. Add `Websocket Security`(wss) Support
- 🍋 `Release(s) 2.2.4.1`
  - File Features
    1. validation, limits (including `permission`, `file size`, `file name length`)
    2. download
    3. upload (client `ajax` upload, server `uuid` file handle)
    4. cache
    5. pagination
- `Pre 2.3.0 to 2.3.1`
  - GeoIP Monitor (User country, request region analysis) v2.3.0-2.3.1
- `Pre 2.3.2-alpha to 2.3.2-beta.2`
  - Instant Message (Websocket Protocol)
- 🌍 `Pre 2.4.0 to 2.4.1`
  - `django-simple-captcha` -> `hCaptcha` verify
- ✈ `Pre 2.5.0 to 2.5.0.2`
   - Improve the performance of code & database
   - User Django-auth
- 🌲 `Pre 2.6.0 to 2.6.0.3`
  - Replit and Vercel deployment 
- 🔥 `Pre 2.7.0-2.7.2.3`
  - Admin Analysis Pages 
    - Users & Requests Region Distribution
    - Server & Website Monitor
- 🌱 `Pre 2.7.3 to 2.7.12`
  - Change Password Page 
  - **Intelligent verification**
    - change password page
    - login page
    - register page
  - User Avatars
  - update Profile Page (`gitee`, `github`, `codepen` info)
- 🎇 `Release 2.7`
- 🍀 `Pre 2.8.0 to 2.8.4.2`
  - dockerfile
  - update `Embedding Applications` structure
  - `SiteApplication` construction
- 📕 `Pre 2.9.0 to 2.9.1`
  - Reduce Photo size (per < 0.6MiB)
- 🚀 `Release 2.10.0 to 2.10.3`
  - `hCaptcha` -> `Cloudflare Turnstile` verify
  - Network attack and defense TEST (php) **Thanks to @APGPerson**
    - fixed file download bug