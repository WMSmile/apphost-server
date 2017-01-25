import socket
import sys
from struct import pack

import server # must be last

sys.path.insert(0, 'dynamic')

class AppHost(object):
    def __init__(self):
        # self.times = {}
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, pack('ii', 0, 0))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("0.0.0.0", 8080))

    def run(self):
        self.socket.listen(5)
        print "running..."
        while True:
            try:
                client, address = self.socket.accept()
                status, headers, body = server.responseHandler.handleReadHeader(client)
                request = status.split(' ')[1]
                method = status.split(' ')[0]

                print 'status', status, 'headers', repr(headers), 'body', repr(body)

                body = server.requestHandler.handleBodyContent(body=body, length=int(headers.get('Content-Length', '0')))

                post = server.requestHandler.handlePOSTRequest(body=body, contentType=headers.get('Content-Type', ''))
                cookie_args, cookie_kwargs = server.requestHandler.handleCookies(cookies=headers.get('Cookie', ""))
                request, get = server.requestHandler.handleGETRequest(request=request)

                client.send(server.responseHandler.handleResponse(request=request, client=client, post_data=post, get_data=get, cookie_args=cookie_args, cookie_kwargs=cookie_kwargs))
                client.shutdown(socket.SHUT_RDWR)
                client.close()
            except KeyboardInterrupt:
                server.eventHandler.handleShutdown(_socket=self.socket)
                break
            except server.NotFoundException as e:
                server.eventHandler.handleNotFound(client=client, errorMessage=e)
            except Exception as e:
                server.eventHandler.handleError(client=client, errorMessage=e)

if __name__ == "__main__":
    apphost = AppHost()
    apphost.run()
    print "\rOK"


