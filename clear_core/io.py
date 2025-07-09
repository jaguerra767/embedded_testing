from __future__ import annotations
from typing import TYPE_CHECKING

# This block is only processed by type checkers, not at runtime.
# It prevents a circular import error because controller.py will import this file.
if TYPE_CHECKING:
    from .controller import ClearCoreController

class IOControl:
    """Handles all digital and analog I/O commands."""
    def __init__(self, controller: 'ClearCoreController'):
        """
        Initializes the IOControl class.

        Args:
            controller: The main ClearCoreController instance to send commands through.
        """
        self._controller = controller

    def set_output_pin(self, pin: int, value: bool) -> str:
        """
        Sets a digital output pin to high (True) or low (False).
        (Note: Command string is hypothetical and may need to be adjusted.)
        """
        state = "1" if value else "0"
        return self._controller._send_command(f"IO{pin}S{state}")

    def read_input_pin(self, pin: int) -> bool:
        """
        Reads the state of a digital input pin. Returns True for high, False for low.
        (Note: Command string is hypothetical and may need to be adjusted.)
        """
        response = self._controller._send_command(f"IO{pin}R")
        # Assuming the controller responds with "1" for high and "0" for low.
        return response.strip() == "1"
