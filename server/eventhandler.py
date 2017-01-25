from traceback import format_exc
from application.error import Error
from responsehandler import ResponseHandler

class EventHandler(object):
    def handleError(self, client, errorMessage):
        traceback = format_exc()
        error = Error().html(error=str(errorMessage), trace=traceback)
        client.send(ResponseHandler()._handleHeaders(response="500 Server Error")+error)

    def handleNotFound(self, client, errorMessage):
        traceback = format_exc()
        error = Error().html(error=str(errorMessage), trace=traceback)
        client.send(ResponseHandler()._handleHeaders(response="404 Not Found")+error)

    def handleShutdown(self, _socket):
        _socket.close()