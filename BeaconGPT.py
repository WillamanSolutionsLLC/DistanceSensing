import bluetooth
from bleak import BleakClient
from bleak import BleakScanner

def calculate_distance(rssi, tx_power):
    """
    Calculate the estimated distance based on the RSSI value and the transmitter power (tx_power).
    This formula provides a rough estimation and may vary depending on the environment and devices used.
    """
    if rssi == 0:
        return -1  # If RSSI is undefined, return -1 indicating an error
    ratio = rssi * 1.0 / tx_power
    if ratio < 1.0:
        return pow(ratio, 10)
    else:
        distance = (0.89976) * pow(ratio, 7.7095) + 0.111
        return distance

def scan_bluetooth_devices(duration=10):
    """
    Scan for Bluetooth devices and print their name, address, and estimated distance.
    The duration parameter specifies the scanning duration in seconds.
    """
    print("Scanning for Bluetooth devices...")
    nearby_devices = bluetooth.discover_devices(duration=duration, lookup_names=True)
    print("Found {} devices".format(len(nearby_devices)))

    for addr, name in nearby_devices:
        rssi = bluetooth.read_rssi(addr)
        distance = calculate_distance(rssi, -59)  # Replace -59 with the transmitter power of your beacon
        print("Device: {}, Address: {}, RSSI: {}, Distance: {:.2f} meters".format(name, addr, rssi, distance))

# Main execution
scan_bluetooth_devices()