import base64
import hashlib
import hmac
import json
import os
import random
import time
from sys import platform
import sys

from .xiaomi_cloud_map_extractor.common.xiaomi_cloud_connector import (
    XiaomiCloudConnector,
)

import requests

if platform != "win32":
    import readline


def GetTokenAndIP(username, password, server):
    servers = ["cn", "de", "us", "ru", "tw", "sg", "in", "i2"]
    servers_str = ", ".join(servers)
    while server not in ["", *servers]:
        raise Exception(f"Invalid server provided. Valid values: {servers_str}")

    if not server == "":
        servers = [server]

    password = base64.urlsafe_b64decode(password).decode("UTF-8")

    connector = XiaomiCloudConnector(username, password)
    logged = connector.login()
    if logged:
        for current_server in servers:
            devices = connector.get_devices(current_server)
            if devices is not None:
                if len(devices["result"]["list"]) == 0:
                    # print(f"No devices found for server \"{current_server}\".")
                    continue
                # print(f"Devices found for server \"{current_server}\":")
                for device in devices["result"]["list"]:
                    # print_tabbed("---------", 3)
                    # if "name" in device:
                    # print_entry("NAME", device["name"], 3)
                    # if "did" in device:
                    #     # print_entry("ID", device["did"], 3)
                    #     if "blt" in device["did"]:
                    #         beaconkey = connector.get_beaconkey(current_server, device["did"])
                    #         if beaconkey and "result" in beaconkey and "beaconkey" in beaconkey["result"]:
                    #             print_entry("BLE KEY", beaconkey["result"]["beaconkey"], 3)

                    ip = ""
                    token = ""
                    if "localip" in device:
                        ip = device["localip"]
                    if "token" in device:
                        token = device["token"]

                    return token, ip
            else:
                raise Exception("Unable to get devices.")
    else:
        raise Exception("Unable to log in.")
