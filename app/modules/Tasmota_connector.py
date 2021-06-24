import os
import sys


script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "..", "..")
sys.path.append(mymodule_dir)

import smartschool.app.modules.data_types.IP as IP


class Tasmota_connector:
    def __init__(self, ip: str, timeout=10, *args, **kwargs):
        self.protocol = "https" if kwargs.get("secure", False) else "http"
        self.address = IP.IP(ip).ip
