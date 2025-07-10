from typing import TYPE_CHECKING


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
        state = "1" if value else "0"
        return self._controller._send_command(f"O{pin}S{state}")

    def read_input_pin(self, pin: int) -> bool:
        """
        Reads the state of a digital input pin. Returns True for high, False for low.
        (Note: Command string is hypothetical and may need to be adjusted.)
        """
        response = self._controller._send_command(f"I{pin}")[3]
        # Assuming the controller responds with "1" for high and "0" for low.
        return response == "1"
