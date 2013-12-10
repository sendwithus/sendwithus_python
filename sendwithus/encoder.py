import datetime
import json
from time import mktime

class SendwithusJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        # Let the base class default method raise the TypeError
        return super(SendwithusJSONEncoder, self).default(obj)
