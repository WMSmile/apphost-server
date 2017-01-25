from apphost import application


class ErrorCard(object):
    def render(self, error, trace, **kwargs):
        return '''<div class="card card-outline-danger error-card" style="margin-top:15px;">
        <div class="card-header">
            <span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i> {message}</span>
        </div>
        <div class="card-block">
            <pre>{traceback}</pre>
        </div>'''.format(
            message=error,
            traceback=trace,
        )

class Error(application.Application):
    def body_content(self, **kwargs):
        return '''<div class="container">
            {error}
        </div>'''.format(
            error=ErrorCard().render(**kwargs),
        )