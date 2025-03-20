import asyncio
from bleak import BleakScanner
import time
from datetime import datetime

class BluetoothDetector:
    def __init__(self):
        self.devices = {}
        self.running = True

    async def scan_devices(self):
        """Scan for nearby Bluetooth devices"""
        try:
            devices = await BleakScanner.discover()
            for device in devices:
                self.devices[device.address] = {
                    'name': device.name or "Unknown",
                    'rssi': device.rssi,
                    'last_seen': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'metadata': device.metadata
                }
        except Exception as e:
            print(f"Error during scanning: {e}")

    def print_devices(self):
        """Print the discovered devices in a formatted way"""
        print("\n" + "="*50)
        print("BLUETOOTH DEVICES DETECTED")
        print("="*50)
        total_devices = len(self.devices)
        print(f"Total Devices Found: {total_devices}")
        print("-"*50)
        if not self.devices:
            print("No devices found")
            return

        for address, info in self.devices.items():
            print(f"\nDevice: {info['name']}")
            print(f"Address: {address}")
            print(f"Signal Strength (RSSI): {info['rssi']} dBm")
            print(f"Last Seen: {info['last_seen']}")
            if info['metadata']:
                print("Additional Info:")
                for key, value in info['metadata'].items():
                    print(f"  {key}: {value}")
        print("\n" + "="*50)

    async def run(self, scan_interval=5):
        """Main loop to continuously scan for devices"""
        print("Starting Bluetooth Scanner...")
        print("Press Ctrl+C to stop")
        try:
            while self.running:
                await self.scan_devices()
                self.print_devices()
                await asyncio.sleep(scan_interval)
        except KeyboardInterrupt:
            print("\nStopping Bluetooth Scanner...")
            self.running = False

def main():
    detector = BluetoothDetector()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(detector.run())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

if __name__ == "__main__":
    main() 