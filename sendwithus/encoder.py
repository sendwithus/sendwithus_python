import datetime
import json
from time import mktime

def swu_json_encode(self, obj):
    if isinstance(obj, datetime.datetime):
        return int(mktime(obj.timetuple()))

    return json.JSONEncoder.default(self, obj)
