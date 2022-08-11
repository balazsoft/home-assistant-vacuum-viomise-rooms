import sys
import binascii
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


import miio
# from custom_components.viomise.miio.protocol import Message

# token = b"43364e35624b7451724c79486b4a375a"
# data = binascii.a2b_hex("213100700000000019914a4600001a52c9a854aa815c5c6062660817a4a035e2ab89b8f741d5afbd52c871730b3d51d3e927a91e5889fcd4e0be379f97856e7c0438831074610b5ff7092872e12ad43f131f2f49a05b9b639486f1e70dcde36aad85704d5f9848c106e80608256ab00c")
# m = Message.parse(data, token=token)
# print(m)

sys.exit(1)

import miio

vac = miio.ViomiVacuum("192.168.137.35", "43364e35624b7451724c79486b4a375a", debug=10)
print(vac)
print(vac.get_current_position())
# print(vac.get_maps())
# vac.start()