
from default_components import DefaultMessage, DefaultHTMLHead, DefaultHTMLBody

class Application(object):
    def html(self, **kwargs):
        return '''<!DOCTYPE html>
<html lang="en">
    {head}
    {body}
</html>'''.format(
            head=self.head(**kwargs),
            body=self.body(**kwargs),
        )

    def body(self, **kwargs):
        return '''<body>
        {content}
    </body>'''.format(
            content=self.body_content(**kwargs),
        )

    def body_content(self, **kwargs):
        return DefaultMessage().render(**kwargs)


    def head(self, **kwargs):
        return '''<head>
            {content}
        </head>'''.format(
            content=self.head_content(**kwargs),
        )

    def head_content(self, **kwargs):
        return DefaultHTMLHead().render(**kwargs)

