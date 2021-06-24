import re

IP_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"


def validate(ip: str):
    ip = ip.strip().replace(" ", "")
    ip = ip.replace("https", "").replace("http", "").replace(":", "").replace("/", "")
    if not re.search(IP_regex, ip):
        raise ValueError("IP not valid (required format 'xxx.yyy.zzz.aaa')")
    return ip


class IP:
    def __init__(self, ip: str):
        self.__ip = validate(ip)

    @property
    def ip(self):
        return self.__ip
