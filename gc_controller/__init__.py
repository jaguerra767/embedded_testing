"""
GameCube Controller Package

This package provides a high-level client for interacting with a GameCube
controller HID device. The main entry point is the GameCubeController class.
"""

# Import the main controller class to make it directly accessible from the package root.
from .controller import GameCubeController

# Import data and enum classes that users of the library may want to access
# for type hinting or state checking.
from .buttons import Button, ButtonsState
from .joystick import JoystickAnalog
from .dpad import DpadDirection

# Define the public API for the package. This controls `from gc_controller import *`
# and helps linters understand the package structure, preventing "unused import" warnings.
__all__ = [
    "GameCubeController",
    "Button",
    "ButtonsState",
    "JoystickAnalog",
    "DpadDirection",
]

__version__ = "2.0.0"
