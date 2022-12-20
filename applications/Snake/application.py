from applications.application import *


@appManager.lazy_setup
class Application(SiteApplication):
    port = 11

# appManager.register_site_application(11, application=Application)