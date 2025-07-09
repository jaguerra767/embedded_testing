# Gantry Control System

This project provides a complete software solution for controlling a gantry system powered by a [Teknic ClearCore Motor Controller](https://www.teknic.com/products/clearcore-motion-and-io-controller/) using a standard USB GameCube controller as a real-time input device.

The system is designed with a modular, object-oriented architecture, making it easy to understand, maintain, and extend.

## Features

- **Real-Time Control:** Low-latency reading of joystick and button inputs to control motor movement.
- **Modular Drivers:** Separate, reusable packages for the `ClearCoreController` (network-based) and `GameCubeController` (USB HID-based).
- **Object-Oriented Design:** Uses a hybrid composition pattern for clean, organized, and scalable code. The main controller classes provide access to specialized sub-controllers (e.g., `controller.motors`, `controller.buttons`).
- **Cross-Platform:** The core Python logic is compatible with both Windows and Linux. (See Linux setup for required hardware permissions).
- **Test Harnesses Included:** Both driver packages include executable `__main__` blocks for standalone testing and diagnostics.
- **Distribution Ready:** Includes instructions for packaging the application into a standalone Windows executable for users without Python installed.

## Project Structure

The project is organized into distinct packages and a main application entry point.

```
embedded_testing/
│
├── demo_gantry/
│   └── main.py              # The main application that integrates the motor and controller.
│
├── clear_core/
│   ├── __init__.py          # Makes 'clear_core' a package.
│   ├── controller.py        # Main ClearCoreController class (manages network).
│   ├── motors.py            # MotorControl class for motor commands.
│   └── io.py                # IOControl class for I/O commands.
│
├── gc_controller/
│   ├── __init__.py          # Makes 'gc_controller' a package.
│   ├── controller.py        # Main GameCubeController class (manages HID device).
│   ├── buttons.py           # Buttons class for digital button states.
│   ├── joystick.py          # Joystick class for analog stick states.
│   └── dpad.py              # Dpad class for the digital D-Pad.
│
└── README.md                # This file.
```

## Setup and Installation

These instructions are for developers who wish to run or modify the source code.

### 1. Prerequisites

- Python 3.8 or newer.
- A USB GameCube Controller Adapter and controller.
- Access to a ClearCore Motor Controller on the network.

### 2. Get the Code

Clone this repository to your local machine:
```bash
git clone <your-repository-url>
cd embedded_testing
```

### 3. Create a Virtual Environment (Recommended)

Using a virtual environment keeps your project dependencies isolated.
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# .venv\Scripts\activate    # On Windows
```

### 4. Install Dependencies

The primary dependency is `hidapi` for USB communication.
```bash
pip install hidapi
```

### 5. **Crucial Linux Setup (udev Rule)**

On Linux, standard users do not have permission to access raw USB devices by default. You must create a `udev` rule to grant access to the GameCube adapter.

1.  Create the rule file (you may need `sudo`):
    ```bash
    sudo nano /etc/udev/rules.d/99-gamecube-adapter.rules
    ```
2.  Add the following line. This targets a common Mayflash adapter. **You may need to change the `idVendor` and `idProduct`** to match your specific hardware.
    ```
    SUBSYSTEM=="usb", ATTRS{idVendor}=="0079", ATTRS{idProduct}=="0006", MODE="0666"
    ```
3.  Reload the udev rules and re-plug your adapter:
    ```bash
    sudo udevadm control --reload-rules && sudo udevadm trigger
    ```

## Usage

### Running the Main Gantry Demo

The main application integrates both controllers. Run it from the root `embedded_testing` directory using Python's module (`-m`) flag.

```bash
python -m demo_gantry.main
```

### Testing the GameCube Controller

You can test the GameCube controller logic independently by running its module directly. This is useful for debugging inputs.

```bash
python -m gc_controller.controller
```

## Distribution for Windows

To share this application with coworkers on Windows who do not have Python, you can package it into a single `.exe` file using **PyInstaller**.

1.  **On a Windows machine**, install PyInstaller in your environment:
    ```bash
    pip install pyinstaller
    ```
2.  From the root `embedded_testing` directory, run the following command:
    ```bash
    pyinstaller --onefile --name GantryControlDemo demo_gantry/main.py
    ```
3.  The standalone executable will be located in the newly created `dist/` folder:
    ```
    dist/GantryControlDemo.exe
    ```
4.  You can send this single `.exe` file to your coworkers. They can run it without installing Python or any libraries.