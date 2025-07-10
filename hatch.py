from clear_core import ClearCoreController
from demo_gantry.hatch import update_hatch

HOST = "192.168.1.12"
PORT = 8888
controller = ClearCoreController(HOST, PORT)
update_hatch(controller)
