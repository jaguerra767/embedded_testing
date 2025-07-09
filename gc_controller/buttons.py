from dataclasses import dataclass
from enum import IntFlag

class Button(IntFlag):
    """
    An IntFlag enum representing all buttons on the controller.

    The values correspond to bit positions in a 16-bit integer formed
    by combining the controller's raw data bytes 5 and 6.
    """
    NONE = 0
    # From byte 5 (lower byte)
    Y = 1 << 4
    X = 1 << 5
    A = 1 << 6
    B = 1 << 7
    # From byte 6 (upper byte, bits shifted by 8)
    L = 1 << 8
    R = 1 << 9
    Z = 1 << 10
    START = 1 << 13

@dataclass(frozen=True, repr=False)
class ButtonsState:
    """An immutable snapshot of the state of all buttons."""
    A: bool
    B: bool
    X: bool
    Y: bool
    L: bool
    R: bool
    Z: bool
    Start: bool

    def __repr__(self) -> str:
        """Provides a compact representation of pressed buttons."""
        pressed = [name for name, is_pressed in self.__dict__.items() if is_pressed]
        return f"ButtonsState({', '.join(pressed) or 'None'})"

class Buttons:
    """
    Parses and holds the state for all digital buttons on the controller.

    This class is stateful and is designed to be updated with new data
    from the main controller on each read cycle.
    """
    def __init__(self):
        self._flags = Button.NONE

    def update(self, byte5: int, byte6: int):
        """Updates the internal button state from the raw controller data bytes."""
        # Combine the two bytes into a single 16-bit integer for easy flag processing.
        combined_value = (byte6 << 8) | byte5
        self._flags = Button(combined_value)

    @property
    def a(self) -> bool:
        """Returns True if the A button is pressed."""
        return Button.A in self._flags

    @property
    def b(self) -> bool:
        """Returns True if the B button is pressed."""
        return Button.B in self._flags

    @property
    def x(self) -> bool:
        """Returns True if the X button is pressed."""
        return Button.X in self._flags

    @property
    def y(self) -> bool:
        """Returns True if the Y button is pressed."""
        return Button.Y in self._flags

    @property
    def l(self) -> bool:
        """Returns True if the L trigger is pressed."""
        return Button.L in self._flags

    @property
    def r(self) -> bool:
        """Returns True if the R trigger is pressed."""
        return Button.R in self._flags

    @property
    def z(self) -> bool:
        """Returns True if the Z button is pressed."""
        return Button.Z in self._flags

    @property
    def start(self) -> bool:
        """Returns True if the Start button is pressed."""
        return Button.START in self._flags

    @property
    def flags(self) -> Button:
        """Returns the raw IntFlag object representing the current state."""
        return self._flags

    @property
    def state(self) -> ButtonsState:
        """Returns an immutable dataclass snapshot of the current button states."""
        return ButtonsState(
            A=self.a, B=self.b, X=self.x, Y=self.y,
            L=self.l, R=self.r, Z=self.z,
            Start=self.start
        )
