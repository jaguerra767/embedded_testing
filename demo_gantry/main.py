import sys
import time
from clear_core import ClearCoreController
from gc_controller import GameCubeController

# --- Constants ---
HOST = "192.168.1.12"
PORT = 8888
GANTRY_ID = 0
MAX_DISPLACEMENT = -80000  # steps
MIN_DISPLACEMENT = 0      # steps

# --- Helper Function ---
def clear_terminal():
    """
    Clears the terminal screen using ANSI escape codes for a flicker-free update.
    """
    # \033[2J clears the entire screen
    # \033[H moves the cursor to the top-left corner
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

# --- Main Application Logic ---
def main():
    """Main function to run the gantry control demo."""
    try:
        # The 'with' statement ensures controllers are properly connected and closed.
        with ClearCoreController(HOST, PORT) as cc, GameCubeController() as gc:
            print("Controllers connected. Initializing gantry...")

            # --- Initial Gantry Setup ---
            if cc.motors.get_status(GANTRY_ID) == 2:  # Status 2 might be 'In Fault'
                print("Motor in fault, clearing alerts...")
                cc.motors.clear_alerts(GANTRY_ID)
                time.sleep(0.5)

            print("Enabling motor...")
            cc.motors.enable(GANTRY_ID)
            time.sleep(0.5)

            if cc.motors.get_position(GANTRY_ID) != 0:
                print("Homing motor to position 0...")
                cc.motors.absolute_move(GANTRY_ID, 0)
                # Wait for the homing move to complete
                while cc.motors.get_status(GANTRY_ID) == 1:  # Status 1 might be 'Moving'
                    time.sleep(0.1)

            print("Initialization complete. Ready for input.")
            time.sleep(1)  # Pause before starting the control loop

            # --- Main Control Loop ---
            while True:
                # gc.read() returns True only when there's new data from the controller.
                if gc.read():
                    # Get all current states at once.
                    current_pos = cc.motors.get_position(GANTRY_ID)
                    joystick_dir = gc.main_stick.direction.name
                    buttons_state = gc.buttons.state
                    motor_status = cc.motors.get_status(GANTRY_ID)

                    # --- Handle Controller Input ---
                    # Move motor based on 'A' button and joystick direction.
                    if buttons_state.A:
                        if joystick_dir == "RIGHT" and current_pos > MAX_DISPLACEMENT:
                            cc.motors.relative_move(GANTRY_ID, -100)
                        elif joystick_dir == "LEFT" and current_pos < MIN_DISPLACEMENT:
                            cc.motors.relative_move(GANTRY_ID, 100)
                        else:
                            # Stop if moving towards a limit or joystick is centered.
                            cc.motors.abrupt_stop(GANTRY_ID)
                    else:
                        # Stop the motor if the 'A' button is not being held.
                        cc.motors.abrupt_stop(GANTRY_ID)

                    # --- Display Current Frame Data ---
                    # Clear the terminal at the beginning of each frame update.
                    clear_terminal()

                    # Build and print the output for the current frame.
                    output_lines = [
                        "--- Gantry Control Demo ---",
                        f"Motor Status:     {motor_status}",
                        f"Gantry Position:  {current_pos}",
                        "",
                        "--- Controller Input ---",
                        f"Joystick:         {joystick_dir}",
                        f"A Button Held:    {buttons_state.A}",
                        "",
                        "Hold 'A' and move Joystick Left/Right to move the gantry.",
                        "Press Ctrl+C to exit."
                    ]
                    print("\n".join(output_lines))

                # A short sleep to be CPU-friendly and set the loop's refresh rate.
                time.sleep(1 / 60)  # Aim for ~60Hz

    except ConnectionError as e:
        print(f"\n[ERROR] A connection error occurred: {e}")
    except KeyboardInterrupt:
        print("\nExiting program.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
