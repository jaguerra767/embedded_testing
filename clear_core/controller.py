import socket
from typing import Optional

# Use relative imports to bring in the other parts of our package
from .motors import MotorControl
from .io import IOControl

class ClearCoreController:
    """
    Main client for the ClearCore motor controller.

    This class manages the network connection and provides access to
    specialized controllers for motors and I/O through its `motors`
    and `io` properties.

    It is recommended to use this class as a context manager with 'with'.
    """
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._sock: Optional[socket.socket] = None

        # The hybrid pattern: instantiate sub-controllers and pass self
        self.motors = MotorControl(self)
        self.io = IOControl(self)

    def connect(self):
        """Establishes the connection to the controller."""
        if self._sock is not None:
            # Avoid reconnecting if already connected
            return
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self.host, self.port))
        except socket.error as e:
            self._sock = None # Ensure state is clean on failure
            # Re-raise the exception for the caller to handle
            raise ConnectionError(f"Failed to connect to {self.host}:{self.port}.") from e

    def close(self):
        """Closes the connection to the controller if it is open."""
        if self._sock:
            self._sock.close()
            self._sock = None

    def __enter__(self):
        """Context manager entry: connects to the device."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit: closes the connection."""
        self.close()

    def _send_command(self, command_body: str) -> str:
        """
        (Internal) Formats and sends a command, then returns the response.
        This is the single point of communication with the hardware.
        """
        if not self._sock:
            raise ConnectionError("Controller is not connected. Call connect() or use a 'with' statement.")

        # Protocol: command is wrapped with Start of Text and End of Text chars
        full_command = f"\x02{command_body}\x13"

        try:
            self._sock.sendall(full_command.encode('ascii'))
            response = self._sock.recv(1024).decode('ascii')
            # It's good practice to strip whitespace/control characters from the response
            return response.strip()
        except socket.error as e:
            # If the connection drops during communication, clean up and raise
            self.close()
            raise ConnectionAbortedError(f"Connection lost while sending command. Error: {e}")
