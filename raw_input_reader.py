#!/usr/bin/env python3
"""
USB GameCube Controller Raw Input Reader
Reads and prints raw HID data from a connected GameCube controller
"""

import hid
import time
import sys

def find_gamecube_controller():
    """Find connected GameCube controller devices"""
    devices = hid.enumerate()
    gc_devices = []

    print("Scanning for HID devices...")
    for device in devices:
        # Common GameCube adapter vendor/product IDs
        # Nintendo GameCube Controller Adapter: 057e:0337
        # Mayflash GameCube Adapter: 0079:1844, 0079:1843
        vendor_id = device['vendor_id']
        product_id = device['product_id']

        print(f"Found device: VID={vendor_id:04x}, PID={product_id:04x}, "
              f"Product: {device.get('product_string', 'Unknown')}")

        # Check for known GameCube adapter IDs or look for "GameCube" in product name
        if ((vendor_id == 0x057e and product_id == 0x0337) or  # Nintendo official
            (vendor_id == 0x0079 and product_id in [0x1844, 0x1843]) or  # Mayflash
            (vendor_id== 0x0079 and product_id == 0x0006) or            # Mayflash
            (device.get('product_string', '').lower().find('gamecube') != -1)):
            gc_devices.append(device)

    return gc_devices

def read_controller_data(device_path):
    """Read raw data from the controller"""
    try:
        # Open the device
        h = hid.device()
        h.open_path(device_path)

        print(f"Connected to: {h.get_manufacturer_string()} {h.get_product_string()}")
        print("Reading controller data (press Ctrl+C to stop)...")
        print("Raw bytes will be displayed as: [byte1, byte2, byte3, ...]")
        print("-" * 60)

        h.set_nonblocking(True)

        while True:
            # Read data (timeout in milliseconds)
            data = h.read(64, timeout_ms=100)

            if data:
                # Print raw bytes
                hex_data = ' '.join([f'{b:02x}' for b in data])
                print(f"Raw: [{', '.join([str(b) for b in data])}]")
                print(f"Hex: {hex_data}")

                # Try to interpret some common button patterns
                if len(data) >= 8:
                    print(f"Interpreted - Bytes 0-7: {data[:8]}")

                print("-" * 40)

            time.sleep(0.01)  # Small delay to prevent spam

    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            h.close()
        except:
            pass

def main():
    # Check if hidapi is available
    try:
        import hid
    except ImportError:
        print("Error: 'hidapi' library not found.")
        print("Install it with: pip install hidapi")
        sys.exit(1)

    print("USB GameCube Controller Reader")
    print("=" * 40)

    # Find GameCube controllers
    devices = find_gamecube_controller()

    if not devices:
        print("\nNo GameCube controllers found!")
        print("Make sure your controller/adapter is connected.")
        print("\nAll connected HID devices:")
        for device in hid.enumerate():
            print(f"  VID={device['vendor_id']:04x}, PID={device['product_id']:04x} - "
                  f"{device.get('product_string', 'Unknown')}")
        return

    # If multiple devices found, let user choose
    if len(devices) > 1:
        print(f"\nFound {len(devices)} GameCube devices:")
        for i, device in enumerate(devices):
            print(f"  {i+1}. {device.get('product_string', 'Unknown')} "
                  f"(VID={device['vendor_id']:04x}, PID={device['product_id']:04x})")

        while True:
            try:
                choice = int(input("Select device (1-{}): ".format(len(devices)))) - 1
                if 0 <= choice < len(devices):
                    selected_device = devices[choice]
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a number!")
    else:
        selected_device = devices[0]

    print(f"\nUsing device: {selected_device.get('product_string', 'Unknown')}")
    read_controller_data(selected_device['path'])

if __name__ == "__main__":
    main()
