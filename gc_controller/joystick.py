from enum import Enum
from dataclasses import dataclass

@dataclass(frozen=True, repr=False)
class JoystickAnalog:
    """
    An immutable snapshot of a joystick's raw analog state.
    Provides X and Y values, typically ranging from 0-255.
    """
    x: int
    y: int

    def __repr__(self) -> str:
        return f"Analog(X={self.x}, Y={self.y})"

class JoystickDirection(Enum):
    """Represents the calculated cardinal and diagonal direction of a joystick."""
    CENTER = "CENTER"
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP_RIGHT = "UP_RIGHT"
    UP_LEFT = "UP_LEFT"
    DOWN_RIGHT = "DOWN_RIGHT"
    DOWN_LEFT = "DOWN_LEFT"

class Joystick:
    """
    Parses and holds the state for a single analog joystick.

    This class is stateful and is designed to be updated with new data
    from the main controller on each read cycle.
    """
    def __init__(self, deadzone: int = 30):
        """
        Initializes the Joystick state.

        Args:
            deadzone: The threshold from the center (128) before movement
                      is registered.
        """
        self._x = 128
        self._y = 128
        self._deadzone = deadzone

    def update(self, x_val: int, y_val: int):
        """Updates the internal state of the joystick from new byte values."""
        self._x = x_val
        self._y = y_val

    @property
    def x(self) -> int:
        """The raw X-axis value (0-255)."""
        return self._x

    @property
    def y(self) -> int:
        """The raw Y-axis value (0-255)."""
        return self._y

    @property
    def analog(self) -> JoystickAnalog:
        """Returns an immutable snapshot of the raw X and Y analog values."""
        return JoystickAnalog(x=self._x, y=self._y)

    @property
    def direction(self) -> JoystickDirection:
        """
        Returns the calculated cardinal or diagonal direction based on
        the current analog values and deadzone.
        """
        center = 128

        # Note: For many controllers, a higher Y value means the stick is pushed UP.
        y_dist = self._y - center
        x_dist = self._x - center

        # Check against the deadzone
        # For this specific controller, a lower Y-value means UP.
        is_up = y_dist < -self._deadzone
        is_down = y_dist > self._deadzone
        is_right = x_dist > self._deadzone
        is_left = x_dist < -self._deadzone

        # Determine direction, prioritizing diagonals
        if is_up:
            if is_right:
                return JoystickDirection.UP_RIGHT
            if is_left:
                return JoystickDirection.UP_LEFT
            return JoystickDirection.UP

        if is_down:
            if is_right:
                return JoystickDirection.DOWN_RIGHT
            if is_left:
                return JoystickDirection.DOWN_LEFT
            return JoystickDirection.DOWN

        # Handle non-diagonal horizontal movement
        if is_right:
            return JoystickDirection.RIGHT
        if is_left:
            return JoystickDirection.LEFT

        return JoystickDirection.CENTER
