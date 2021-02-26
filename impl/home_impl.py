from datetime import timedelta

from core.exception import FormatError


# def send_embed_response(data):


def parse_time_duration(time):
    try:
        unit = time[-1:]
        print(unit)
        num = int(time[:-1])
        print(num)
        kwarg = dict()
        if unit == 'm' and 60 > num > 0:
            kwarg['minutes'] = num
        elif unit == 'h' and 24 > num > 0:
            kwarg['hours'] = num
        elif unit == 'd' and 7 > num > 0:
            kwarg['days'] = num
        else:
            raise FormatError
        return timedelta(**kwarg)
    except ValueError:
        raise FormatError
