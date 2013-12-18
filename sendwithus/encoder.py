import datetime
import decimal
import json
from time import mktime


class SendwithusJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        # Let the base class default method raise the TypeError
        return super(SendwithusJSONEncoder, self).default(obj)
