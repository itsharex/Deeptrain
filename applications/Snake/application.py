from applications.application import *


@appManager.register
class Application(SiteApplication):
    port = 11
