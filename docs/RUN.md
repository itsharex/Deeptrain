# 🍉 QuickStart 🍎
1. ## 🌏 Docker 🌏
   - #### Dockerfile (Container Mode - `SQLite` + `LocMem`)
     ```commandline
     docker build -t zmh .
     docker run -p 8000:8000 -t zmh
     ```
   - #### Docker-compose (Compose Mode - `MySQL` + `Redis` + `Nginx`)
     ```commandline
     docker-compose up
     ```
2. ## 🍏 Native 🍏
    1. #### Production
       - Initialize
          *(there is no need to make migrations)*
          ```commandline
          pip install -r requirements.txt
          python manage.py migrate
          ```
       - Run
          ```commandline
            python manage.py
          ```

   2. #### Deployment
      1. initialize
         https://github.com/zmh-program/Zh-Website/blob/main/DjangoWebsite/settings.py#L41
         ```commandline
          pip install -r requirements.txt

          python manage.py migrate
          python manage.py collectstatic
         ```
      2. run
         ```commandline
         gunicorn -c gunicorn.conf.py DjangoWebsite.wsgi:application
         ```

## 🚘 Commands 🚜
- Create Superuser [identity: `Server-Owner`]
  - >(*same as command `createsuperuser`*)
    >```commandline
    >python manage.py buildsuperuser
    >```
- Create Admin (identity: `Admin`)
  - >(*same as command `createsuperuser`*)
    >```commandline
    >python manage.py buildadmin
    >```


## 📮 Configs 🎨

https://github.com/zmh-program/Zh-Website/blob/7a44e9597a40d7407e1fe8c9c995663c266eecc8/config.json#L1-L18

## 📕 Settings 📚

*⚠ initialize then!*

https://github.com/zmh-program/Zh-Website/blob/aac95dbd5a1ae9a0b64a245063538e4567f07d72/DjangoWebsite/settings.py#L114

rewrite to

```python
IS_CONTAINER = False
```

- `MySQL`

  https://github.com/zmh-program/Zh-Website/blob/aac95dbd5a1ae9a0b64a245063538e4567f07d72/DjangoWebsite/settings.py#L133-L143

  > ```sql
  > create DATABASE `django-database`;
  > ```
  >
- `Redis`

  https://github.com/zmh-program/Zh-Website/blob/aac95dbd5a1ae9a0b64a245063538e4567f07d72/DjangoWebsite/settings.py#L145-L154
