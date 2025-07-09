from __future__ import annotations
from typing import TYPE_CHECKING
from enum import IntEnum

# This block is only processed by type checkers, not at runtime.
# It prevents a circular import error because controller.py will import this file.
if TYPE_CHECKING:
    from .controller import ClearCoreController



class Status(IntEnum):
    DISABLED = 0
    ENABLING = 1
    FAULTED = 2
    READY = 3
    MOVING = 4

class MotorControl:
    """Handles all motor-related commands."""
    def __init__(self, controller: 'ClearCoreController'):
        """
        Initializes the MotorControl class.

        Args:
            controller: The main ClearCoreController instance to send commands through.
        """
        self._controller = controller

    def enable(self, motor: int) -> str:
        """Enables a specific motor."""
        return self._controller._send_command(f"M{motor}EN")

    def disable(self, motor: int) -> str:
        """Disables a specific motor."""
        return self._controller._send_command(f"M{motor}DE")

    def absolute_move(self, motor: int, steps: int) -> str:
        """Moves a motor to an absolute position specified by steps."""
        return self._controller._send_command(f"M{motor}AM{steps}")

    def relative_move(self, motor: int, steps: int) -> str:
        """Moves a motor by a relative number of steps."""
        return self._controller._send_command(f"M{motor}RM{steps}")

    def clear_alerts(self, motor: int) -> str:
        """Clears any alerts associated with a specific motor."""
        return self._controller._send_command(f"M{motor}CA")

    def get_position(self, motor: int) -> int:
        """Gets the current position of a motor."""
        response = self._controller._send_command(f"M{motor}GP")[3:]
        return int(response.strip())

    def set_velocity(self, motor:int, velo: int) -> str:
        return self._controller._send_command(f"M{motor}SV{velo}")
    
    def set_acceleration(self, motor:int, accel: int) -> str:
        return self._controller._send_command(f"M{motor}SA{accel}")

    def set_deceleration(self, motor:int, decel: int) ->str:
        return self._controller._send_command(f"M{motor}SD{decel}")

    def get_status(self, motor: int) -> Status:
        """Gets the status of a motor."""
        response = int(self._controller._send_command(f"M{motor}GS")[3:])
        return Status(response)

    def abrupt_stop(self, motor: int) -> str:
        """Stops a motor abruptly."""
        return self._controller._send_command(f"M{motor}AS")
