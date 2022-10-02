from applications.application import appHandler, UserApplication, JSONApplicationConsumer


class Application(UserApplication):
    name = "Snake"
    author = "张铭瀚"
    profile = """Online Snake Game!"""
    github_addr = "https://github.com/zmh-program/Zh-Website"
    image = "https://cdn-icons-png.flaticon.com/128/3245/3245498.png"


@appHandler.register(Application)
class Consumer(JSONApplicationConsumer):
    pass
