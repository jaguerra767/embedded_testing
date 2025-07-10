from enum import IntFlag
from dataclasses import dataclass

from clear_core.controller import ClearCoreController


HATCH_MOTOR_ID = 1
PE_SENSOR_ID = 6
OPEN_SENSOR_ID = 1
CLOSE_SENSOR_ID = 2


OPEN_STROKE = -100000
CLOSE_STROKE = 100000

class Action(IntFlag):
    OPEN = 1
    CLOSE = 0

@dataclass
class MoveParameters:
    stroke: int
    sensor_id: int

def select_params(action: Action):
    if action == Action.OPEN:
        print("Opening hatch")
        return MoveParameters(OPEN_STROKE, OPEN_SENSOR_ID)
    elif action == Action.CLOSE:
        print("Closing hatch")
        return MoveParameters(CLOSE_STROKE, CLOSE_SENSOR_ID)

def update_hatch(controller: ClearCoreController):
    hatch_ready = controller.motors.get_status(HATCH_MOTOR_ID) == 3
    params = select_params(Action(controller.io.read_input_pin(PE_SENSOR_ID)))
    in_position_res = controller.io.read_input_pin(params.sensor_id)
    print(in_position_res)
    if in_position_res:
        print("Hatch in position")
        #controller.motors.abrupt_stop(HATCH_MOTOR_ID)
    elif hatch_ready:
        #controller.motors.relative_move(HATCH_MOTOR_ID, params.stroke)
        pass
