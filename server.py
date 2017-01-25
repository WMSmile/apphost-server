import sys
import socket
import time
from os.path import isfile
from os import stat as fstat
from traceback import format_exc
from struct import pack
from urlparse import parse_qs
reload(sys)
from sys import setdefaultencoding
from application.error import Error
setdefaultencoding('utf-8')
sys.path.insert(0, 'dynamic')


class NotFoundException(Exception):
    pass

class AppHost(object):
    def __init__(self):
        self.times = {}
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, pack('ii', 0, 0))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("0.0.0.0", 8080))

    def _importTemplate(self, request, **kwargs):
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

    def _headers(self, extra=[], response="200 OK", contentType="text/html"):
        header = "HTTP/1.0 {0}\r\n".format(response)
        for h in extra:
            if "Location" in h:
                header = "HTTP/1.0 302 Redirect\r\n"
        header += "Date: " + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) + "\r\n"
        header += "Server: AppHost 0.5\r\n"
        #header += "Content-Type: \"{0}\"\r\n".format(contentType)
        for h in extra:
            header += "%s\r\n" % h
        header += "Connection: close\r\n\r\n"
        return header.encode()

    def _contentFromImport(self, page, **kwargs):
            page_main = getattr(page, "main")
            content, headers = page_main(**kwargs)
            return (content + "\r\n", headers)

    def _loadResponse(self, request, **kwargs):
        request = request or "index"
        share = ['.css', '.js', '.ttf', '.woff', '.woff2', '.ico', '.jpg', '.jpeg', 'png', '.tiff', '.svg']

        # Special Files
        for s in share:
            if request.endswith(s):
                return self._headers() + open("share/%s" % request, 'r').read()

        # Normal Page
        page = self._importTemplate(request, **kwargs)
        content, headers = self._contentFromImport(page)
        return self._headers(extra=headers) + content


    def _readHeader(self, client):
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

    def run(self):
        self.socket.listen(5)
        run = True
        print "running..."
        while run:
            try:
                client, address = self.socket.accept()
                status, headers, body = self._readHeader(client)
                print 'status', status, 'headers', repr(headers), 'body', repr(body)
                method = status.split(' ')[0]
                length = int(headers.get('Content-Length', '0'))
                if length > len(body):
                    print "recieving", length
                    body += client.recv(length)
                args = {}
                if "application/x-www-form-urlencoded" == headers.get('Content-Type', ''):
                    args = parse_qs(body)
                    print args
                cookies = headers.get('Cookie', "").split('; ')
                for cookie in cookies:
                    if not cookie.strip():
                        continue
                    k, v = cookie.split('=', 1)
                    args[k] = v
                request = status.split(' ')[1]
                if "?" in request:
                    request, _args = request.split('?', 1)
                    _args = parse_qs(_args)
                    for k, v in _args.iteritems():
                        args[k] = v
                print "sending"
                client.send(self._loadResponse(request[1:], client=client, **args))
                print "sent"
                client.shutdown(socket.SHUT_RDWR)
                client.close()
                print "duty fullfilled"
            except KeyboardInterrupt:
                run = False
                self.socket.close()
                self.socket.shutdown(socket.SHUT_RDWR)
            except Exception as e:
                traceback = format_exc()
                error = Error().html(error=str(e), trace=traceback) + "\r\n"
                client.send(self._headers()+error)
                # run = False
                # print str(format_exc())
                # exit()
                #self.http500(client, error=str(e))

if __name__ == "__main__":
    server = AppHost()
    server.run()
    print("OK")


