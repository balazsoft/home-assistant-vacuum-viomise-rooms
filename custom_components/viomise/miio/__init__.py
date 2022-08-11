# flake8: noqa
try:
    # python 3.7 and earlier
    from importlib_metadata import version  # type: ignore
except ImportError:
    # python 3.8 and later
    from importlib.metadata import version  # type: ignore

from custom_components.viomise.miio.airconditioner_miot import AirConditionerMiot
from custom_components.viomise.miio.airconditioningcompanion import (
    AirConditioningCompanion,
    AirConditioningCompanionV3,
)
from custom_components.viomise.miio.airconditioningcompanionMCN import (
    AirConditioningCompanionMcn02,
)
from custom_components.viomise.miio.airdehumidifier import AirDehumidifier
from custom_components.viomise.miio.airfresh import AirFresh, AirFreshVA4
from custom_components.viomise.miio.airfresh_t2017 import AirFreshA1, AirFreshT2017
from custom_components.viomise.miio.airhumidifier import (
    AirHumidifier,
    AirHumidifierCA1,
    AirHumidifierCB1,
)
from custom_components.viomise.miio.airhumidifier_jsq import AirHumidifierJsq
from custom_components.viomise.miio.airhumidifier_miot import AirHumidifierMiot
from custom_components.viomise.miio.airhumidifier_mjjsq import AirHumidifierMjjsq
from custom_components.viomise.miio.airpurifier import AirPurifier
from custom_components.viomise.miio.airpurifier_airdog import (
    AirDogX3,
    AirDogX5,
    AirDogX7SM,
)
from custom_components.viomise.miio.airpurifier_miot import (
    AirPurifierMB4,
    AirPurifierMiot,
)
from custom_components.viomise.miio.airqualitymonitor import AirQualityMonitor
from custom_components.viomise.miio.airqualitymonitor_miot import AirQualityMonitorCGDN1
from custom_components.viomise.miio.aqaracamera import AqaraCamera
from custom_components.viomise.miio.ceil import Ceil
from custom_components.viomise.miio.chuangmi_camera import ChuangmiCamera
from custom_components.viomise.miio.chuangmi_ir import ChuangmiIr
from custom_components.viomise.miio.chuangmi_plug import (
    ChuangmiPlug,
    Plug,
    PlugV1,
    PlugV3,
)
from custom_components.viomise.miio.cooker import Cooker
from custom_components.viomise.miio.curtain_youpin import CurtainMiot
from custom_components.viomise.miio.device import Device, DeviceStatus
from custom_components.viomise.miio.exceptions import DeviceError, DeviceException
from custom_components.viomise.miio.fan import Fan, FanP5, FanSA1, FanV2, FanZA1, FanZA4
from custom_components.viomise.miio.fan_leshow import FanLeshow
from custom_components.viomise.miio.fan_miot import (
    Fan1C,
    FanMiot,
    FanP9,
    FanP10,
    FanP11,
    FanZA5,
)
from custom_components.viomise.miio.gateway import Gateway
from custom_components.viomise.miio.heater import Heater
from custom_components.viomise.miio.heater_miot import HeaterMiot
from custom_components.viomise.miio.huizuo import (
    Huizuo,
    HuizuoLampFan,
    HuizuoLampHeater,
    HuizuoLampScene,
)
from custom_components.viomise.miio.integrations.petwaterdispenser import (
    PetWaterDispenser,
)
from custom_components.viomise.miio.integrations.vacuum.dreame.dreamevacuum_miot import (
    DreameVacuumMiot,
)
from custom_components.viomise.miio.integrations.vacuum.mijia import G1Vacuum
from custom_components.viomise.miio.integrations.vacuum.roborock import (
    RoborockVacuum,
    Vacuum,
    VacuumException,
)
from custom_components.viomise.miio.integrations.vacuum.roborock.vacuumcontainers import (
    CleaningDetails,
    CleaningSummary,
    ConsumableStatus,
    DNDStatus,
    Timer,
    VacuumStatus,
)
from custom_components.viomise.miio.integrations.vacuum.roidmi.roidmivacuum_miot import (
    RoidmiVacuumMiot,
)
from custom_components.viomise.miio.integrations.vacuum.viomi.viomivacuum import (
    ViomiVacuum,
)
from custom_components.viomise.miio.integrations.yeelight import Yeelight
from custom_components.viomise.miio.miot_device import MiotDevice
from custom_components.viomise.miio.philips_bulb import PhilipsBulb, PhilipsWhiteBulb
from custom_components.viomise.miio.philips_eyecare import PhilipsEyecare
from custom_components.viomise.miio.philips_moonlight import PhilipsMoonlight
from custom_components.viomise.miio.philips_rwread import PhilipsRwread
from custom_components.viomise.miio.powerstrip import PowerStrip
from custom_components.viomise.miio.protocol import Message, Utils
from custom_components.viomise.miio.pwzn_relay import PwznRelay
from custom_components.viomise.miio.scishare_coffeemaker import ScishareCoffee
from custom_components.viomise.miio.toiletlid import Toiletlid
from custom_components.viomise.miio.walkingpad import Walkingpad
from custom_components.viomise.miio.waterpurifier import WaterPurifier
from custom_components.viomise.miio.waterpurifier_yunmi import WaterPurifierYunmi
from custom_components.viomise.miio.wifirepeater import WifiRepeater
from custom_components.viomise.miio.wifispeaker import WifiSpeaker
from custom_components.viomise.miio.yeelight_dual_switch import (
    YeelightDualControlModule,
)

from custom_components.viomise.miio.discovery import Discovery

__version__ = version("python-miio")
