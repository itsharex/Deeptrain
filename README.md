# Zh Website
![GitHub forks](https://img.shields.io/github/forks/zmh-program/Zh-Website)
![GitHub Repo stars](https://img.shields.io/github/stars/zmh-program/Zh-Website)
![GitHub repo size](https://img.shields.io/github/repo-size/zmh-program/Zh-Website)
![GitHub repo file count](https://img.shields.io/github/directory-file-count/zmh-program/Zh-Website)
![GitHub](https://img.shields.io/github/license/zmh-program/Zh-Website)

[![star](https://gitee.com/zmh-program/Zh-Website/badge/star.svg?theme=dark)](https://gitee.com/zmh-program/Zh-Website/stargazers)
[![fork](https://gitee.com/zmh-program/Zh-Website/badge/fork.svg?theme=dark)](https://gitee.com/zmh-program/Zh-Website/members)
> 🧡Django Website, and you can extend applications in the website.

<br></br>
## Application Analysis Map
![map](/preview/application.jpg)
## 🚀️预览 | ScreenShot

![banner](/preview/main-banner.PNG)
![app](/preview/emapp.PNG)
![features](/preview/main-features.PNG)
![website info](/preview/main-info.PNG)
![profile](/preview/profile.PNG)
![profile page](/preview/profile-page.PNG)
![register](/preview/register.PNG)
 See the full preview at the *Website Features* below
## 🍉用前须知 | Before Using

- `MySQL` `localhost:3306`
  > DjangoWebsite / settings.py / line:94

- `Redis` `127.0.0.1:6379`
  > DjangoWebsite / settings.py / line:107 & line:83

- `Unix/Linux system`
- `python 3.7+`

## ✈快速开始 | QuickStart
  *(run in the parent directory)*
> mysql
> ```sql
> create DATABASE `django-database`;
> ```

>command line
> ```commandline
> cd Zh-Website
> pip install -r requirements.txt
> 
> python manage.py makemigrations
> python manage.py migrate
> 
> python manage.py collectstatic
> ```


## 网站功能 | Website Features
1. **User**
  - login
    ![login](/preview/login.PNG)
    ![login-mobile](/preview/login-mobile.PNG)
  - register
    ![register](/preview/register.PNG)
    ![register-mobile](/preview/register-mobile.PNG)
  - change password
    ![change](/preview/change.PNG)
    ![change-mobile](/preview/change-mobile.PNG)
  - profile
    ![profile](/preview/profile.PNG)
    ![profile-page](/preview/profile-page.PNG)
2. **Files**
    ![upload](/preview/upload.PNG)
    ![uploading](/preview/uploading.PNG)
    ![fileupload](/preview/uploadfile.PNG)
    ![file](/preview/file.PNG)

3. **Admin** (django-SimpleUi)
![simpleui](/preview/simpleui.PNG)
![monitor](/preview/monitor.PNG)
![geoip](/preview/geoip.PNG)
![github-pages](/preview/github-page.PNG)

4. Chat room
![chat](/preview/chat.png)
![chat-2](/preview/chat-2.PNG)

5. Database
  - MySQL (or sqlite3) database

6. Cache
  - Redis

8. **内嵌式应用程序 | Embedded Applications**

![applications](/preview/emapp.PNG)

> Easy to use applications - No need to change other files(outside this application directory), and <`application.appHandler`> automatically calls
>
> 快速使用app - 不需要更改此app程序父目录外的任何文件, `appHandler`会自动调用

- `startapp.py` 快速创建与搭建应用程序 | easy to create applications

> `startapp.py` 使用`rich`控制台美化 | use `rich.console`

- `applications/application.py`
- `appHandler` 应用程序管理 | Application Manager
- `UserApplication` 应用程序类 | Application Class
  > `AbstractApplication` -> `UserApplication`
  >
- `JSONApplicationConsumer` 应用程序用户类 | Application User Class
  > `channels.generic.websocket.WebsocketConsumer` -> `AbstractApplicationConsumer` -> `JSONApplicationConsumer`
  >
- 应用程序信息 | Application Information
  > `app-name 名称`，`author 作者`， `profile 简介`, `github-address 地址`，`ASGISupport`，`WSGISupport`
  >
