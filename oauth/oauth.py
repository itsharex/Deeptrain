from ssl import SSLError
from urllib.parse import urlencode
import oauth2
from typing import *
from json import loads
from django.contrib import auth
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.functional import cached_property
from django.urls import path
from .models import OAuthModel


class OAuthApplicationManager(object):
    """
    like:
        /oauth/callback/github/
    """

    def __init__(self, *apps):
        self.apps: List["OAuthApplication"] = [app() for app in apps]

    @property
    def urlpatterns(self):
        return [app.app_path for app in self.apps]

    @cached_property
    def template(self) -> List[Dict[str, str]]:
        return [{"name": app.APPNAME, "icon": app.ICON, "url": app.authorize_url} for app in self.apps]


class OAuthApplication(object):
    APPNAME = ""
    SITEKEY = ""
    SECRET = ""
    SITE_URL = ""
    TOKEN_URL = ""

    ICON = ""

    def __init__(self):
        self.consumer = oauth2.Consumer(
            key=self.SITEKEY,
            secret=self.SECRET,
        )
        self.client = oauth2.Client(self.consumer)

        print(self.authorize_url)

    @cached_property
    def authorize_url(self):
        return f"{self.SITE_URL}/authorize?client_id={self.SITEKEY}"

    def verify_url(self, code):
        pass

    @property
    def app_path(self):
        return path(f"callback/{self.APPNAME.lower()}/", self.callback_view, name=self.APPNAME)

    def handle_api(self, api: dict, request: WSGIRequest):
        oauth_id = api.get("id")
        oauth_name = api.get("login")
        user = request.user
        if oauth_name and oauth_id:
            if not user.is_authenticated:  # 作为第三方登录, 在cookies/sessions未储存用户模型实例, 即未登录状态, 查询已注册的oauth数据库
                query = OAuthModel.objects.filter(oauth_id=oauth_id, oauth_name=oauth_name, oauth_app=self.APPNAME)
                if query.exists():
                    auth.login(request, query.first().user)
                    return {"success": True}
                else:
                    return {"success": False, "reason": "OAuth authentication failed"}
            else:  # 状态已登录, 设置绑定 OAuth App
                OAuthModel.objects.create(user=user, oauth_id=oauth_id, oauth_name=oauth_name)
                return {"success": True}

    def callback(self, request: WSGIRequest):
        pass

    def callback_view(self, request: WSGIRequest):
        return JsonResponse(self.callback(request))

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

    SITEKEY = "05b353c81e2c15bf148d"  # Client ID
    SECRET = "69e7f754938df94ae9ba9743a48c76a831e9e7cd"  # Client Secrets
    SITE_URL = "https://github.com/login/oauth"
    TOKEN_URL = "https://api.github.com/user"

    ICON = "https://www.flaticon.com/free-icon/github_5968866"

    def __init__(self):
        super().__init__()

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
            return {"success": False, "reason": "Timed out"}
        return {"success": False, "reason": "Code is empty"}


class GiteeOAuthApplication(OAuthApplication):
    """
    Gitee OAuth Docs:
        https://gitee.com/api/v5/oauth_doc#/
    """

    APPNAME = "Gitee"

    SITEKEY = "a0fa985b1e26127f188285d69de2b66b3de8ed03a50e11866acb1a1d595c92fd"  # Client ID
    SECRET = "3786a2b1f9d6b77e6ba3079613ac4e76ff388b32d98f2d110fa845f1d0eaedc6"  # Client Secret
    SITE_URL = "https://gitee.com/oauth"
    TOKEN_URL = "https://gitee.com/api/v5/user"

    REDIRECT_URI = "http://zmh.site:8000/oauth/callback/gitee/"  # 设置gitee回调地址(必须) 可以设置本机hosts文件 将域名dns至本机

    ICON = "https://gitee.com/static/images/logo.svg"

    def __init__(self):
        super().__init__()

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
            return {"success": False, "reason": "Timed out"}
        return {"success": False, "reason": "Code is empty"}


oauthManager = OAuthApplicationManager(
    GithubOAuthApplication,
    GiteeOAuthApplication,
)
