import time
from clear_core import ClearCoreController
from demo_gantry.hatch import HATCH_MOTOR_ID, update_hatch


if __name__=="__main__":
    HOST = "192.168.1.12"
    PORT = 8888
    controller = ClearCoreController(HOST, PORT)
    with controller as cc:
        try:
            cc.motors.enable(HATCH_MOTOR_ID)
            while True:
                update_hatch(cc)
                time.sleep(0.1)
        except ConnectionError as e:
            print(f"\n[ERROR] A connection error occurred: {e}")
        except KeyboardInterrupt:
            print("\nExiting program.")
        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred: {e}")
