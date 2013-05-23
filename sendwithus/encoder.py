import logging
import datetime
from time import mktime
import json

FORMAT = '%(asctime)-15s %(message)s'
logger = logging.getLogger('sendwithus')
logger.propagate = False

def swu_json_encode(self, obj):
    if isinstance(obj, datetime.datetime):
        return int(mktime(obj.timetuple()))

    return json.JSONEncoder.default(self, obj)

