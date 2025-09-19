import datetime

def timestamp():
    return datetime.datetime.now().strftime(('%Y-%m-%d %H:%M:%S'))


def serialize_objectid(object):
    object['_id'] = str(object['_id'])
    return object