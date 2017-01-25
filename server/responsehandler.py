import time
from os.path import isfile
from os import stat as fstat


class ResponseHandler(object):
    def __init__(self):
        self.times = {}


    def handleReadHeader(self, client):
        data = client.recv(1024)
        while True:
            if not data:
                break
            print "data:",len(data), repr(data)
            if "\r\n\r\n" in data:
                break
            data += client.recv(1024)
        status, data = data.split('\r\n', 1)
        headers, body = data.split("\r\n\r\n", 1)
        headers =  dict([h.strip().title(), v.strip()] for (h, v) in (h.split(':', 1) for h in headers.split("\r\n")))
        return status, headers, body


    def handleResponse(self, request, **kwargs):
        request = request[1:]
        request = request or "index"

        share = ['.css', '.js', '.ttf', '.woff', '.woff2', '.ico', '.jpg', '.jpeg', 'png', '.tiff', '.svg']

        for s in share:
            if request.endswith(s):
                return self._handleHeaders(**kwargs) + open("share/%s" % request, 'r').read()

        page = self._handleTemplate(request, **kwargs)
        content, headers = self._handleImport(page)
        return self._handleHeaders(extra=headers, **kwargs) + content + "\r\n"


    def _handleHeaders(self, extra=[], response="200 OK", contentType="text/html", **kwargs):
        header = "HTTP/1.0 {0}\r\n".format(response)
        for h in extra:
            if "Location" in h:
                header = "HTTP/1.0 302 Redirect\r\n"
        header += "Date: " + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) + "\r\n"
        header += "Server: AppHost 0.5\r\n"
        #header += "Content-Type: {0}\r\n".format(contentType)
        for h in extra:
            header += "%s\r\n" % h
        header += "Connection: close\r\n\r\n"
        return header.encode()


    def _handleTemplate(self, request, **kwargs):
        template = "dynamic/{template_file}.py".format(template_file=request)
        if not isfile(template):
            raise NotFoundException("Not found \"%s\"" % template)
        if not self.times.get(request, False):
            self.times[request] = fstat(template).st_mtime
        old = self.times[request]
        new = fstat(template).st_mtime
        page = __import__(request)
        if not old == new:
            self.times[request] = fstat(template).st_mtime
            reload(page)
        return page


    def _handleImport(self, page, **kwargs):
            page_main = getattr(page, "main")
            content, headers = page_main(**kwargs)
            return (content + "\r\n", headers)



class NotFoundException(Exception):
    pass