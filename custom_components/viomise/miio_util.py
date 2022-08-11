import asyncio
from datetime import time
import sys
import binascii
import logging
import time
import base64
from functools import partial


from custom_components.viomise import token_extractor

from custom_components.viomise import miio
from custom_components.viomise.miio.integrations.vacuum.viomi.viomivacuum import (
    ViomiMovementDirection,
)
from custom_components.viomise.miio.protocol import Message
from custom_components.viomise.miio import RoborockVacuum, DeviceException

from custom_components.viomise.xiaomi_cloud_map_extractor.common.xiaomi_cloud_connector import (
    XiaomiCloudConnector,
)
from custom_components.viomise.xiaomi_cloud_map_extractor.viomi.vacuum import (
    ViomiVacuum,
)
from custom_components.viomise.xiaomi_cloud_map_extractor.viomi.map_data_parser import (
    MapDataParserViomi,
)

# try:
#     from custom_components.viomise.miio import RoborockVacuum, DeviceException
# except ImportError:
#     from custom_components.viomise.miio import Vacuum as RoborockVacuum, DeviceException
import zlib

_LOGGER = logging.getLogger(__name__)

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)

# def decryptData(data, token):
#     token = binascii.a2b_hex(token)
#     data = binascii.a2b_hex(data)
#     m = Message.parse(data, token=token)
#     print(m)

# token = "43364e35624b7451724c79486b4a375a"
# data = "213100700000000019914a4600001a52c9a854aa815c5c6062660817a4a035e2ab89b8f741d5afbd52c871730b3d51d3e927a91e5889fcd4e0be379f97856e7c0438831074610b5ff7092872e12ad43f131f2f49a05b9b639486f1e70dcde36aad85704d5f9848c106e80608256ab00c"

# decryptData(data, token)

# sys.exit(1)
class ViomiSE3Rooms:
    def __init__(self, host, token, username, password, country):
        self.token = token
        self.ip = host
        self._country = country
        self.username = username
        self.password = password

        self.rooms = None

        self._logged_in = False
        self.checkConnection()

    # async def _try_command(self, mask_error, func, *args, **kwargs):
    #     """Call a func handling error messages."""
    #     try:
    #         await self.hass.async_add_executor_job(partial(func, *args, **kwargs))
    #         return True
    #     except DeviceException as exc:
    #         _LOGGER.error(mask_error, exc)
    #         return False

    def checkConnection(self):
        if self._logged_in == False:
            try:
                self.vac = miio.ViomiVacuum(self.ip, self.token, debug=0)
                self.checkViomiVacuum(
                    self.username,
                    base64.urlsafe_b64encode(self.password.encode()).decode("UTF-8"),
                    self._country,
                )

                self._vacuum = RoborockVacuum(self.ip, self.token)
                self._connector = XiaomiCloudConnector(self.username, self.password)
                self._logged_in = self._connector.login()
            except Exception as exc:
                _LOGGER.error("CheckConnection: %s", exc)
                return False

            if self._logged_in:
                country, user_id, device_id, model = self._connector.get_device_details(
                    self._vacuum.token, self._country
                )
                if model is not None:
                    self._country = country
                    self._device = self._create_device(user_id, device_id, model)
                else:
                    return False
            else:
                return False

    def getRooms(self):
        if self.checkConnection() == False:
            return []

        if self.rooms == None:
            self.getPosition()

        ret = []

        for i in self.rooms:
            ret.append(
                (
                    self.rooms[i].name,
                    self.rooms[i].number,
                    self.rooms[i].x0,
                    self.rooms[i].y0,
                    self.rooms[i].x1,
                    self.rooms[i].y1,
                )
            )

        return ret

    def getPosition(self):
        counter = 10
        map_name = self._handle_map_name(counter)
        response = self._device.get_raw_map_data(map_name)

        unzipped = zlib.decompress(response)
        colors = [1]
        drawables = [1]
        texts = [
            {
                "text": "Room 1",
                "x": 25,
                "y": 25,
                "color": (125, 20, 213),
                "font": "FreeSans.ttf",
                "font_size": 25,
            },
            {
                "text": "Room 2",
                "x": 25,
                "y": 75,
                "color": (125, 20, 213),
                "font": "FreeSans.ttf",
                "font_size": 25,
            },
        ]
        sizes = [1]
        image_config = {
            "scale": 20,
            "rotate": 180,
            "trim": {"top": 10, "bottom": 20, "left": 30, "right": 40},
        }
        map_data = MapDataParserViomi.parse(
            unzipped, colors, drawables, texts, sizes, image_config
        )
        self.rooms = map_data.rooms
        return (map_data.vacuum_position.x, map_data.vacuum_position.y)

    def _handle_map_name(self, counter):
        map_name = "retry"
        if self._device is not None and not self._device.should_get_map_from_vacuum():
            map_name = "0"
        while map_name == "retry" and counter > 0:
            _LOGGER.debug("Retrieving map name from device")
            time.sleep(0.1)
            try:
                map_name = self._vacuum.map()[0]
                _LOGGER.debug("Map name %s", map_name)
            except OSError as exc:
                _LOGGER.error("Got OSError while fetching the state: %s", exc)
            except DeviceException as exc:
                if self._received_map_name_previously:
                    _LOGGER.warning("Got exception while fetching the state: %s", exc)
                self._received_map_name_previously = False
            finally:
                counter = counter - 1
        return map_name

    def _create_device(self, user_id, device_id, model):
        self._used_api = "viomi"
        return ViomiVacuum(self._connector, self._country, user_id, device_id, model)

    def checkViomiVacuum(self, user, password, country):
        try:
            self.vac.info()
        except DeviceException as exc:
            orgIP = self.vac.ip
            toReplace = 'ip = "{0}"'
            if str(exc).find("Unable to discover the device") == 0:
                self.token, self.ip = token_extractor.GetTokenAndIP(
                    user, password, country
                )
                self.vac = miio.ViomiVacuum(self.ip, self.token, debug=0)
                self.vac.info()

                f = open(__file__, "r+")
                all = f.read()
                all = all.replace(
                    toReplace.format(orgIP), toReplace.format(self.vac.ip)
                )
                f.seek(0, 0)
                f.write(all)
                f.close()
            else:
                raise exc

    # def getRooms(self):
    #     maps = self.vac.get_maps()
    #     self.vac.set_map(maps[0]["id"])

    #     rooms = {}
    #     for map in maps:
    #         floor = {}
    #         floor.update(self.vac.get_rooms(map_id = map["id"]))
    #         rooms[map["id"]] = floor

    #     return rooms

    def cleanRooms(self, rooms):
        self.vac.start_with_room(rooms)

    def stop(self):
        self.vac.stop()

    def home(self):
        self.vac.home()

    def getStatus(self):
        return self.vac.status()

    def info(self):
        return self.vac.send("miIO.info")


# class ViomiSE3Map():
#     def __init__(self):
#         self._vacuum = RoborockVacuum(host, token)
#         password = base64.urlsafe_b64decode(password).decode("UTF-8")
#         self._connector = XiaomiCloudConnector(username, password)
#         self._logged_in = self._connector.login()
#         country, user_id, device_id, model = self._connector.get_device_details(self._vacuum.token, self._country)
#         if model is not None:
#             self._country = country
#             self._device = self._create_device(user_id, device_id, model)
#         # print(map_name)

#     def getPosition(self):
#         counter = 10
#         map_name = self._handle_map_name(counter)
#         response = self._device.get_raw_map_data(map_name)

#         unzipped = zlib.decompress(response)
#         colors = [1]
#         drawables = [1]
#         texts = [
#             {
#                 "text" : "Room 1",
#                 "x" : 25,
#                 "y" : 25,
#                 "color" : (125, 20, 213),
#                 "font": "FreeSans.ttf",
#                 "font_size": 25
#             },
#             {
#                 "text" : "Room 2",
#                 "x" : 25,
#                 "y" : 75,
#                 "color" : (125, 20, 213),
#                 "font": "FreeSans.ttf",
#                 "font_size": 25
#             }
#         ]
#         sizes = [1]
#         image_config = {
#             "scale": 20,
#             "rotate": 180,
#             "trim": {
#         "top" : 10,
#         "bottom" : 20,
#         "left" : 30,
#         "right" : 40}}
#         map_data = MapDataParserViomi.parse(unzipped, colors, drawables, texts, sizes, image_config)
#         print(map_data.vacuum_position.x)
#         print(map_data.vacuum_position.y)

#     def _handle_map_name(self, counter):
#         map_name = "retry"
#         if self._device is not None and not self._device.should_get_map_from_vacuum():
#             map_name = "0"
#         while map_name == "retry" and counter > 0:
#             _LOGGER.debug("Retrieving map name from device")
#             time.sleep(0.1)
#             try:
#                 map_name = self._vacuum.map()[0]
#                 _LOGGER.debug("Map name %s", map_name)
#             except OSError as exc:
#                 _LOGGER.error("Got OSError while fetching the state: %s", exc)
#             except DeviceException as exc:
#                 if self._received_map_name_previously:
#                     _LOGGER.warning("Got exception while fetching the state: %s", exc)
#                 self._received_map_name_previously = False
#             finally:
#                 counter = counter - 1
#         return map_name

#     def _create_device(self, user_id, device_id, model):
#         self._used_api = "viomi"
#         return ViomiVacuum(self._connector, self._country, user_id, device_id, model)


# print(vac)
# print(vac.get_current_position())
# print(vac.get_maps())
# vac.start()
# vac.start_with_room([1])
# vac.get_rooms()
# vac.clean_mode(miio.integrations.vacuum.viomi.viomivacuum.ViomiMode.Vacuum)
# vac.status()
# vac.get_properties(["run_state","mode","err_state","battary_life","box_type","mop_type","s_time","s_area","suction_grade","water_grade","remember_map","has_map","is_mop","has_newmap"])
# vac.get_properties([""], property_getter= "get_prop")
# vac.dnd_status()


# vac.home() #ok
# vac.info() #ok
# vac.pause() #ok
# vac.stop() #ok
# vac.start_with_room(["Bath", "Lobby"]) #ok
# print(vac.get_rooms()) #ok


# - 0 (0=Normal Vacuum, 1=Edge only)
# - 1 (Don’t know what it does, have to test it, maybe number of passages)
# - 1 (Quantity of rooms)
# - 14 (Room ID)
# vac.send("set_mode_withroom", [0, 1, 1, 1]) #ok

# vac.clean_mode(miio.integrations.vacuum.viomi.viomivacuum.ViomiMode.Vacuum)
# vac.send("set_mop", [0])
# vac.send("set_suction", [0])

# vac.move(ViomiMovementDirection.Forward, duration = 5)

# vac.send("set_direction", [1,1,1]) #ok ?


# vac.send("get_map") #ok  {'id': 1, 'result': {'out': [{'piid': 11, 'value': '[{"name":"Map1","id":1640004279,"cur":true}]'}], 'code': 0}, 'exe_time': 701}
# vac.send("set_carpetturbo", [2]) #ok?
# vac.send("get_ordertime") #ok
# vac.send("miIO.info") #ok

# maps = vac.get_maps()
# vac.set_map(maps[0]["id"])

# for map in maps:
#     print(map["id"])
#     print(vac.get_rooms(map_id = map["id"]))


# if True:
#     vac.home() #ok
# else:

#     vac.send("set_direction", [ViomiMovementDirection.Right.value])
#     vac.send("set_direction", [ViomiMovementDirection.Right.value])


#     # vac.move(ViomiMovementDirection.Forward, duration = 4)
#     # vac.move(ViomiMovementDirection.Right, duration = turn_360/4)
#     # vac.move(ViomiMovementDirection.Forward, duration = 10)
#     # vac.move(ViomiMovementDirection.Right, duration = turn_360/4)
#     # vac.move(ViomiMovementDirection.Forward, duration = 5)
#     # vac.move(ViomiMovementDirection.Right, duration = turn_360/4)
#     # vac.move(ViomiMovementDirection.Forward, duration = 2)

#     # vac.move(ViomiMovementDirection.Right, duration = turn_360/4)
#     # vac.move(ViomiMovementDirection.Forward, duration = 2)
