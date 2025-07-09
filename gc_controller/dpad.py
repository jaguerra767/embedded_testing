from enum import Enum

class DpadDirection(Enum):
    """Represents the 4 cardinal directions of the D-Pad."""
    CENTER = "Center"
    UP = "Up"
    DOWN = "Down"
    LEFT = "Left"
    RIGHT = "Right"

class Dpad:
    """
    Parses and holds the state of the 4-way digital D-Pad.

    This class is stateful and is designed to be updated with new data
    from the main controller on each read cycle. It interprets the state
    from the numerical value of the lower 4 bits of a data byte,
    and includes logic to handle specific hardware quirks.
    """
    def __init__(self):
        # A value of 8 or higher is typically used for the released/centered state.
        self._value = 8

    def update(self, byte_val: int):
        """
        Updates the D-Pad state from the low nibble of a given byte.

        Args:
            byte_val: The byte containing the D-Pad state (typically data[5]).
        """
        # The D-Pad state is encoded in the lower 4 bits (the "nibble").
        self._value = byte_val & 0x0F

    @property
    def direction(self) -> DpadDirection:
        """
        Returns the current direction of the D-Pad, correcting for hardware quirks.
        """
        # This mapping handles a specific hardware quirk where "Up" and "Down"
        # incorrectly report a "Left" component. We explicitly map these
        # quirky values (7 and 5) to their intended cardinal directions.
        if self._value == 7:
            return DpadDirection.UP
        elif self._value == 5:
            return DpadDirection.DOWN
        elif self._value == 6:
            return DpadDirection.LEFT
        elif self._value == 2:
            return DpadDirection.RIGHT
        # The cardinal directions for UP (0) and DOWN (4) are added as a fallback
        # in case the hardware behaves correctly under some circumstances.
        elif self._value == 0:
            return DpadDirection.UP
        elif self._value == 4:
            return DpadDirection.DOWN
        else:
            # Any other value is treated as center.
            return DpadDirection.CENTER
