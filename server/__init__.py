from server.requesthandler import RequestHandler
from server.eventhandler import EventHandler
from server.responsehandler import ResponseHandler, NotFoundException

import sys
reload(sys)
from sys import setdefaultencoding
setdefaultencoding('utf-8')

eventHandler = EventHandler()
requestHandler = RequestHandler()
responseHandler = ResponseHandler()