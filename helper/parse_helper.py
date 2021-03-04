import re
from datetime import timedelta

from core.exception import FormatError


class DurationParser:
    def __init__(self, time):
        regex = re.compile(r'^((?P<days>\d+?)d)?((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?$')
        self.time = dict()
        try:
            parts = regex.match(time)
            if parts is None:
                raise FormatError
            self.time = {name: int(param) for name, param in parts.groupdict().items() if param}
            print(parts.groupdict())
        except ValueError:
            raise FormatError

    def get_time(self):
        return timedelta(**self.time)

    def get_str(self):
        time_str = ''
        if 'days' in self.time.keys():
            time_str += f' {self.time["days"]}天'
        if 'hours' in self.time.keys():
            time_str += f' {self.time["hours"]}小時'
        if 'minutes' in self.time.keys():
            time_str += f' {self.time["minutes"]}分'
        if 'seconds' in self.time.keys():
            time_str += f' {self.time["seconds"]}秒'
        return time_str

