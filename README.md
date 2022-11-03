# Zh Website

> 🧡Django Website, and you can extend applications in the website.

<br></br>

## 🚀️预览 | Preview

![banner](/preview/main-banner.PNG)
![cookies](/preview/cookies-adt.PNG)
![app](/preview/emapp.PNG)
![features](/preview/main-features.PNG)
![website info](/preview/main-info.PNG)
![profile](/preview/profile.PNG)
![profile page](/preview/profile-page.PNG)
![register](/preview/register.PNG)

## 🍉用前须知 | Before Using

- 确保已在 `localhost:3306`运行 `MySQL`， 且用户名与密码都符合

> 更改处 | Replacement `DjangoWebsite / settings.py / line:94`

- 确保在 `127.0.0.1:6379`运行 `Redis`

> 更改处 | Replacement `DjangoWebsite / settings.py / line:107` 与 `DjangoWebsite / settings.py / line:83`

- 初始化 | Initialize
  *run in the parent directory*
> ```sql
> create DATABASE `django-database`
> ```
> ```commandline
> python manage.py makemigrations
> python manage.py migrate
> python manage.py collectstatic
> ```


- 模块 | Module Requirements

  ```
    asgiref==3.5.2
    async-timeout==4.0.2
    cffi==1.15.1
    cryptography==38.0.1
    Deprecated==1.2.13
    Django==3.2.16
    django-redis==5.2.0
    django-simpleui==2022.7.29
    importlib-metadata==5.0.0
    jwt==1.3.1
    packaging==21.3
    pycparser==2.21
    PyJWT==2.6.0
    PyMySQL==1.0.2
    pyparsing==3.0.9
    pytz==2022.5
    redis==4.3.4
    six==1.16.0
    sqlparse==0.4.3
    typing_extensions==4.4.0
    wincertstore==0.2
    wrapt==1.14.1
    zipp==3.10.0
    rich==12.5.1
  ```
- 环境问题 | Environment
  -`linux system`

## 网站功能 | Website Features

1.**内嵌式应用程序 | Embedded Applications**

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

2.**用户功能 | User Features**

- `注册 Register` | `登录 Login` `登出 Logout` | `Cookies自动登录提示 Cookies automatic logon prompt`
- Cookies
- JSON Web Token
- `简介 Profile` <--> User
- `身份概念 ID`
- 0: User 普通用户
- 1:  VIP VIP用户(仅次于Admin)
- 2: Admin 管理员
- 3: Server Owner 服主

> `@login_required` 用户登录过滤封装

3.管理员界面 | Admin Page

- `django - Simple Ui`

4. Dwebsocket

`IM Server` - chat room 在线聊天室

5.数据库 Database `MySQL`
DjangoWebsite / settings.py / line:94

```python
DATABASES = {  
'default':  
      {  
'ENGINE': 'django.db.backends.mysql', # module  
'NAME': 'django-database', # database name  
'HOST': 'localhost', # ip  
'PORT': 3306,  
'USER': 'root',  
'PASSWORD': 'zmh200904',  
}  
}
```

6. 缓存 | Cache `Redis`
   DjangoWebsite / settings.py / line:107

```python
CACHES = {  
    "default": {  
    "BACKEND": "django_redis.cache.RedisCache",  
    "LOCATION": "redis://127.0.0.1:6379/",  
    "OPTIONS": {  
    "CLIENT_CLASS": "django_redis.client.DefaultClient",  
    }  
    }  
  }
```
