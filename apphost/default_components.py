
class DefaultMessage(object):
    def render(cls, title="My Application", **kwargs):
        return '''<div class="jumbotron">
            <h1>{0}</h1>
        </div>'''.format(title)

class DefaultHTMLBody(object):
    def render(self, **kwargs):
        return '''<body>
            {content}
            {scripts}
        </body>'''.format(
            content=self.body_content(**kwargs),
        )

    def body_content(self, **kwargs):
        return DefaultMessage().render(**kwargs)

class DefaultHTMLHead(object):
    def render(self, **kwargs):
        return '''
    <head>
        {content}
    </head>
        '''.format(
            content=self.head_content(**kwargs),
        )

    def head_content(self, **kwargs):
        return '''
        {charset}
        {mobile}
        {jquery}
        {tether}
        {bootstrap}
        {icons}
        {style}
        {script}
        '''.format(
            charset=self.charset().render(**kwargs),
            mobile=self.mobile().render(**kwargs),
            jquery=self.jquery().render(**kwargs),
            tether=self.tether().render(**kwargs),
            bootstrap=self.bootstrap().render(**kwargs),
            icons=self.icon_pack().render(**kwargs),
            style=self.stylesheet().render(**kwargs),
            script=self.javascript().render(**kwargs),
        )

    def mobile(self):
        return MobileApp()

    def charset(self):
        return UTF8Charset()

    def jquery(self):
        return JQuery()

    def tether(self):
        return Tether()

    def stylesheet(self):
        return ApplicationCSS()

    def javascript(self):
        return ApplicationJS()

    def bootstrap(self):
        return Bootstrap()

    def icon_pack(self):
        return FontAwesome()



class Bootstrap(object):
    def render(self, **kwargs):
        return '''<script src="/js/bootstrap4.min.js" type="text/javascript"></script>
        <link rel="stylesheet" type="text/css" href="/css/bootstrap4.min.css">'''

class ApplicationCSS(object):
    def render(self, **kwargs):
        return '''<link rel="stylesheet" type="text/css" href="/css/application.css">'''

class FontAwesome(object):
    def render(self, **kwargs):
        return '''<link rel="stylesheet" type="text/css" href="/css/font-awesome.min.css">'''

class ApplicationJS(object):
    def render(self, **kwargs):
        return '''<script src="/js/application.js" type="text/javascript"></script>'''

class JQuery(object):
    def render(self, **kwargs):
        return '''<script src="/js/jquery3.1.1.min.js" type="text/javascript"></script>'''

class JQueryCDN(object):
    def render(self, **kwargs):
        return '''<script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script>'''

class Tether(object):
    def render(self, **kwargs):
        return '''<script src="/js/tether1.4.0.min.js" type="text/javascript"></script>'''

class TetherCDN(object):
    def render(self, **kwargs):
        return '''<script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>'''

class BootstrapCDN(object):
    def render(self, **kwargs):
        return '''<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>'''

class UTF8Charset(object):
    def render(self, **kwargs):
        return '''<meta charset="utf-8">'''

class MobileApp(object):
    def render(self, **kwargs):
        return '''<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">'''




