import datetime, os, logging, traceback
from config import LOGSLOCATION

from django.shortcuts import redirect
from django.http import JsonResponse

#---------Logger for Exception --------------#                                                                                                                                                                            
exception_logger = logging.getLogger('exception.logs')
exception_hdlr = logging.FileHandler(LOGSLOCATION + "exception.logs", mode='a', encoding=None, delay=False)
exception_hdlr.setFormatter(logging.Formatter('%(asctime)s,%(message)s'))
exception_logger.addHandler(exception_hdlr)
exception_logger.setLevel(logging.DEBUG)
#--------------------------------------------#

class exceptionCheckMiddleware(object):
    # the middleware will be added to the onion layer of middlewares in settings and any exception will raise a status 500
	# to the frontend while logging and informing the internal tech team etc.
	def __init__(self, get_response=None):
	    self.get_response = get_response

	def process_exception(self,request,exception):
		path = request.get_full_path()
		error = traceback.format_exc()
		error = error.replace('\n','`\n`')
		msg = "`Error while loading {0} page: Error: {1}, request user is {2}`".format(path, error, request.user)
        # send_msg_somewhere(msg)
		exception_logger.info('{},{},{}'.format(path,request.user,exception))	
		return JsonResponse({'result':False, 'error': error}, status=500)