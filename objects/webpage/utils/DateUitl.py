import datetime

def get_uuid_by_minute() -> str:
    d = datetime.datetime.now()
    return str('{:0>2d}'.format(d.month)) + str('{:0>2d}'.format(d.day)) + str('{:0>2d}'.format(d.hour)) + str \
        ('{:0>2d}'.format(d.minute))
