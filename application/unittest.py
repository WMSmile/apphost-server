from apphost import application
from apphost import default_components

class CustomHTMLHead(default_components.DefaultHTMLHead):
    def jquery(self):
        return default_components.JQueryCDN()

    def tether(self):
        return default_components.TetherCDN()

    def bootstrap(self):
        return default_components.BootstrapCDN()

class Unittest(application.Application):
    def head_content(self, **kwargs):
        return CustomHTMLHead().render(**kwargs)