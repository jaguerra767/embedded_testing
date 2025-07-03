#!/usr/bin/env python3
"""
HID Device Checker - Check if a device supports HID interface
Works on Windows, macOS, and Linux
"""

import sys

def check_hid_support():
    """Check what HID devices are available on the system"""

    # Try to import hidapi
    try:
        import hid
        print("✓ HID library available")
    except ImportError:
        print("✗ HID library not found. Install with: pip install hidapi")
        return False

    print("\n" + "="*60)
    print("SCANNING FOR ALL HID DEVICES")
    print("="*60)

    devices = hid.enumerate()

    if not devices:
        print("No HID devices found!")
        return False

    print(f"Found {len(devices)} HID devices:\n")

    gamecube_keywords = ['gamecube', 'gc', 'nintendo', 'mayflash', 'controller']
    potential_gc_devices = []

    for i, device in enumerate(devices, 1):
        vendor_id = device['vendor_id']
        product_id = device['product_id']
        manufacturer = device.get('manufacturer_string', 'Unknown')
        product = device.get('product_string', 'Unknown')
        path = device['path']

        print(f"{i:2d}. VID: {vendor_id:04X} PID: {product_id:04X}")
        print(f"    Manufacturer: {manufacturer}")
        print(f"    Product:      {product}")
        print(f"    Path:         {path}")

        # Check if this might be a GameCube controller
        device_text = f"{manufacturer} {product}".lower()
        is_potential_gc = any(keyword in device_text for keyword in gamecube_keywords)

        # Check known GameCube adapter IDs
        known_gc_ids = [
            (0x057e, 0x0337),  # Nintendo GameCube Controller Adapter
            (0x0079, 0x1844),  # Mayflash GameCube Adapter
            (0x0079, 0x1843),  # Mayflash GameCube Adapter (alternate)
        ]

        if (vendor_id, product_id) in known_gc_ids or is_potential_gc:
            print("    >>> POTENTIAL GAMECUBE DEVICE <<<")
            potential_gc_devices.append((i, device))

        print()

    # Test connectivity for potential GameCube devices
    if potential_gc_devices:
        print("="*60)
        print("TESTING POTENTIAL GAMECUBE DEVICES")
        print("="*60)

        for device_num, device in potential_gc_devices:
            print(f"\nTesting device #{device_num}: {device.get('product_string', 'Unknown')}")
            test_hid_connectivity(device)

    return True

def test_hid_connectivity(device):
    """Test if we can actually connect to and read from a HID device"""
    try:
        import hid
        h = hid.device()

        print("  Attempting to open device...")
        h.open_path(device['path'])

        print("  ✓ Successfully opened!")
        print(f"  ✓ Manufacturer: {h.get_manufacturer_string()}")
        print(f"  ✓ Product: {h.get_product_string()}")
        print(f"  ✓ Serial: {h.get_serial_number_string()}")

        # Try to read some data (non-blocking)
        h.set_nonblocking(True)
        print("  Testing data read...")

        data = h.read(64, timeout_ms=1000)
        if data:
            print(f"  ✓ Successfully read {len(data)} bytes: {data[:8]}...")
        else:
            print("  ⚠ No data received (device might be idle)")

        print("  ✓ Device is HID-compatible and accessible!")

        h.close()
        return True

    except Exception as e:
        print(f"  ✗ Error accessing device: {e}")
        return False

def check_system_info():
    """Display system-specific HID information"""
    import platform

    print("SYSTEM HID INFORMATION")
    print("="*60)
    print(f"Platform: {platform.system()} {platform.release()}")

    if platform.system() == "Linux":
        print("\nLinux HID paths:")
        try:
            import os
            if os.path.exists("/dev/input/"):
                devices = [f for f in os.listdir("/dev/input/") if f.startswith("event")]
                print(f"  Input devices: {devices}")

            if os.path.exists("/sys/class/input/"):
                devices = os.listdir("/sys/class/input/")
                print(f"  Input classes: {devices[:10]}...")  # Show first 10
        except Exception as e:
            print(f"  Could not read input devices: {e}")

    elif platform.system() == "Windows":
        print("\nWindows: Check Device Manager > Human Interface Devices")

    elif platform.system() == "Darwin":
        print("\nmacOS: Check System Information > Hardware > USB")

    print()

def main():
    print("HID DEVICE CHECKER")
    print("="*60)
    print("This tool will help you determine if your GameCube controller")
    print("supports HID interface for reading raw input data.")
    print("\nPress Ctrl+C to exit at any time.\n")

    check_system_info()

    if not check_hid_support():
        return

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("If you saw 'POTENTIAL GAMECUBE DEVICE' above and it passed")
    print("the connectivity test, your controller supports HID!")
    print("\nNext steps:")
    print("1. Use the GameCube controller reader script")
    print("2. Press buttons while the script runs to see raw data")
    print("3. The raw bytes will help you understand the controller's protocol")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
