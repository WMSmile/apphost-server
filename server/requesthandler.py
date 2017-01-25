from urlparse import parse_qs

class RequestHandler():
    def handleCookies(self, cookies):
        cookie_args = []
        cookie_kwargs = {}

        for cookie in cookies.split('; '):
            if not cookie.strip():
                continue
            elif not '=' in cookie:
                result['cookie_args'].append(cookie)
            else:
                k, v = cookie.split('=', 1)
                result['cookie_kwargs'][k]=v
        return (cookie_args, cookie_kwargs)


    def handlePOSTRequest(self, contentType, body):
        result = {}
        if contentType == "application/x-www-form-urlencoded":
            result = parse_qs(body)
        return result


    def handleBodyContent(self, body, length):
        if length > len(body):
            body += client.recv(length)
        return body

    def handleGETRequest(self, request):
        get_kwargs = {}
        _request = request
        if "?" in request:
            _request, _args = request.split('?', 1)
            get_kwargs = parse_qs(_args)

        return (_request, get_kwargs)