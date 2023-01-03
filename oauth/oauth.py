from ssl import SSLError
from urllib.parse import urlencode
import oauth2
from typing import *
from json import loads
from django.contrib import auth
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render
from django.utils.functional import cached_property
from django.urls import path
from user.models import User
from .models import OAuthModel
from DjangoWebsite.settings import OAUTH_CONFIG
#  from views import throw_bad_request   未初始化导入问题


class OAuthApplicationManager(object):
    """
    like:
        /oauth/callback/github/
    """
    apps: List["OAuthApplication"]

    def __init__(self, config):
        self.apps = []

        for app_type, conf in config.items():
            app = OAuthTypeSupport.get(app_type)
            if app:
                self.apps.append(app(**conf))

    @property
    def urlpatterns(self):
        return [app.app_path for app in self.apps]

    @cached_property
    def login_template(self) -> List[Dict[str, str]]:
        return [app.get_login_template() for app in self.apps]

    def bind_template(self, user: User):
        return [app.get_bind_template(user) for app in self.apps]


class OAuthApplication(object):
    APPNAME = ""
    SITEKEY = ""
    SECRET = ""
    SITE_URL = ""
    TOKEN_URL = ""

    ICON = ""

    def __init__(self, SITEKEY, SECRET):
        self.SITEKEY = SITEKEY
        self.SECRET = SECRET

        self.consumer = oauth2.Consumer(
            key=self.SITEKEY,
            secret=self.SECRET,
        )
        self.client = oauth2.Client(self.consumer)

    @cached_property
    def authorize_url(self):
        return f"{self.SITE_URL}/authorize?client_id={self.SITEKEY}"

    def verify_url(self, code):
        pass

    @property
    def app_path(self):
        return path(f"callback/{self.APPNAME.lower()}/", self.callback, name=self.APPNAME)

    def get_oauth_username(self, user: User) -> Union[bool, str]:
        query = OAuthModel.objects.filter(oauth_app=self.APPNAME, user=user)
        if not query.exists():
            return False
        return query.first().oauth_name

    def get_login_template(self):
        return {
            "name": self.APPNAME,
            "icon": self.ICON,
            "url": self.authorize_url,
        }

    def get_bind_template(self, user: User):
        resp = self.get_oauth_username(user)
        authorized = resp is not False

        return {
            "name": self.APPNAME,
            "icon": self.ICON,
            "url": self.authorize_url,
            "authorize": authorized,
            "username": resp,
        }

    def handle_api(self, api: dict, request: WSGIRequest):
        oauth_id = api.get("id")
        oauth_name = api.get("login")
        user = request.user
        if not (oauth_name and oauth_id):
            return
        if not user.is_authenticated:  # 作为第三方登录, 在cookies/sessions未储存用户模型实例, 即未登录状态, 查询已注册的oauth数据库
            query = OAuthModel.objects.filter(oauth_id=oauth_id, oauth_name=oauth_name, oauth_app=self.APPNAME)
            if query.exists():
                auth.login(request, query.first().user)
                return redirect("/home/")
            else:
                return throw_bad_request(request, "OAuth authentication failed")
        else:  # 状态已登录, 设置绑定 OAuth App
            OAuthModel.objects.create(user=user, oauth_id=oauth_id, oauth_name=oauth_name, oauth_app=self.APPNAME)
            return redirect("/oauth/bind/")

    def callback(self, request: WSGIRequest):
        pass

    def parse_content(self, content) -> bool:
        pass


class GithubOAuthApplication(OAuthApplication):
    """
    GitHub OAuth Docs:
        https://docs.github.com/zh/developers/apps/building-oauth-apps

    Token -> API like:
        {"login":"zmh-program","id":112773885,
        "node_id":"U_kgDOBrjK_Q","avatar_url":"https://avatars.githubusercontent.com/u/112773885?v=4",
        "gravatar_id":"","url":"https://api.github.com/users/zmh-program",
        "html_url":"https://github.com/zmh-program",
        "followers_url":"https://api.github.com/users/zmh-program/followers",
        "following_url":"https://api.github.com/users/zmh-program/following{/other_user}",
        "gists_url":"https://api.github.com/users/zmh-program/gists{/gist_id}",
        "starred_url":"https://api.github.com/users/zmh-program/starred{/owner}{/repo}",
        "subscriptions_url":"https://api.github.com/users/zmh-program/subscriptions",
        "organizations_url":"https://api.github.com/users/zmh-program/orgs",
        "repos_url":"https://api.github.com/users/zmh-program/repos",
        "events_url":"https://api.github.com/users/zmh-program/events{/privacy}",
        "received_events_url":"https://api.github.com/users/zmh-program/received_events","type":"User",
        "site_admin":false,"name":"Zhang Minghan","company":null,"blog":"zmh-program.site","location":"China",
        "email":null,"hireable":null,"bio":null,"twitter_username":null,"public_repos":10,"public_gists":0,
        "followers":0,"following":1,"created_at":"2022-09-03T17:01:31Z","updated_at":"2022-12-27T12:54:08Z"}
    """

    APPNAME = "GitHub"

    SITEKEY: str  # Client ID
    SECRET: str   # Client Secrets

    SITE_URL = "https://github.com/login/oauth"
    TOKEN_URL = "https://api.github.com/user"

    ICON = "https://cdn-icons-png.flaticon.com/128/5968/5968810.png"

    def verify_url(self, code):
        params = urlencode({
            'client_id': self.SITEKEY,
            'client_secret': self.SECRET,
            'code': code,
        })
        return f"{self.SITE_URL}/access_token?{params}"

    def callback(self, request: WSGIRequest):
        code = request.GET.get("code")
        if code:
            try:
                response, content = self.client.request(self.verify_url(code), headers={
                    'accept': 'application/json',
                })
                if response.status == 200:
                    token = loads(content).get("access_token")
                    token_response, token_content = self.client.request(self.TOKEN_URL, headers={
                        "accept": 'application/json',
                        "Authorization": f"Bearer {token}",
                    })
                    if token_response.status == 200:
                        return self.handle_api(loads(token_content), request)
            except (TimeoutError, SSLError):
                pass
            return throw_bad_request(request, "Timed out")
        return throw_bad_request(request, "Code is empty")


class GiteeOAuthApplication(OAuthApplication):
    """
    Gitee OAuth Docs:
        https://gitee.com/api/v5/oauth_doc#/
    """

    APPNAME = "Gitee"

    SITEKEY: str  # Client ID
    SECRET: str   # Client Secret
    SITE_URL = "https://gitee.com/oauth"
    TOKEN_URL = "https://gitee.com/api/v5/user"

    REDIRECT_URI = "http://zmh.site:8000/oauth/callback/gitee/"  # 设置gitee回调地址(必须) 可以设置本机hosts文件 将域名dns至本机

    ICON = "https://gitee.com/favicon.ico"

    @cached_property
    def authorize_url(self):
        return f"{self.SITE_URL}/authorize?client_id={self.SITEKEY}&response_type=code&redirect_uri={self.REDIRECT_URI}"

    def verify_url(self, code):
        #  https://gitee.com/oauth/token?grant_type=authorization_code&code=...&client_id=...&redirect_uri=...&client_secret=...
        params = urlencode({
            'grant_type': 'authorization_code',
            'client_id': self.SITEKEY,
            'client_secret': self.SECRET,
            'code': code,
            'redirect_uri': self.REDIRECT_URI,
        })
        return f"{self.SITE_URL}/token?{params}"

    def callback(self, request: WSGIRequest):
        code = request.GET.get("code")
        if code:
            try:
                response, content = self.client.request(self.verify_url(code), headers={
                    'accept': 'application/json',
                }, method="POST")
                if response.status == 200:
                    token = loads(content).get("access_token")
                    token_response, token_content = self.client.request(self.TOKEN_URL, headers={
                        "accept": 'application/json',
                        "Authorization": f"Bearer {token}",
                    })
                    if token_response.status == 200:
                        return self.handle_api(loads(token_content), request)
            except (TimeoutError, SSLError):
                pass
            return throw_bad_request(request, "Timed out")
        return throw_bad_request(request, "Code is empty")


OAuthTypeSupport = {
    "GitHub": GithubOAuthApplication,
    "Gitee": GiteeOAuthApplication,
}

oauthManager = OAuthApplicationManager(
    OAUTH_CONFIG,
)
