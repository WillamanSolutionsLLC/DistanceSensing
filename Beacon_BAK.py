import datetime
import time
import math
import simplejson
import asyncio
from bleak import BleakClient
from bleak import BleakScanner

device_uuid = "69FCD0C1-1FA5-9211-6200-B6C5432F459B"
truck_name = 'ORM-2034'
device_names = ['BLDEMO']
show_distance = True
show_stoplight = True
slight_pause = False
red_light = 3
yellow_light = 10
green_light = 20
red_color_code = 'red'
yellow_color_code = 'yellow'
green_color_code = 'green'
black_color_code = 'black'
n = 3
mp = -69


def get_distance_meters(rssi):
    return round(10 ** ((mp - (int(rssi)))/(10 * n)), 2)


def get_distance_feet(rssi):
    return get_distance_meters(rssi) * 3.280839895


def calculate_distance(tx_power, rssi):
    distance = math.pow(10, (tx_power-rssi)/30)

    return distance * 3.280839895

def update_stoplight(beacon_distance):
    if green_light >= beacon_distance > yellow_light:
        background_color = 'green'
    elif yellow_light >= beacon_distance > red_light:
        background_color = 'yellow'
    elif beacon_distance <= red_light:
        background_color = 'red'
    else:
        background_color = 'black'

    return background_color


def update_stoplight_data(beacon_distance, stoplight_color, truck_name):
    with open('data.json', 'w') as f:
        simplejson.dump({'color': stoplight_color, 'distance': beacon_distance, 'truck_id': truck_name}, f)


async def main():
    while True:
        device = await BleakScanner.find_device_by_address(device_uuid, timeout=1)
        if device is not None:
            beacon_distance = get_distance_feet(device.rssi)
            dist_2 = calculate_distance(0, device.rssi)
            if show_distance:
                print(f"\tRSSI: {device.rssi} -- Distance: {beacon_distance} Distance2: {dist_2}-- {datetime.datetime.now()}")
            if show_stoplight:
                stoplight_color = update_stoplight(beacon_distance)
                update_stoplight_data(beacon_distance, stoplight_color, truck_name)
                print(f"\tStoplight Color: {stoplight_color} -- {datetime.datetime.now()}")

        if slight_pause:
            time.sleep(.1)


async def scan_and_get_all_information():
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name in device_names:
            try:
                this_device = await BleakScanner.find_device_by_address(device.address, timeout=20)
                async with BleakClient(this_device) as client:
                    print(f'Services found for device {device.name}:')
                    print(f'\tName:{device.name}')
                    print(f'\tAddress:{device.address}')
                    print(f"\tMetadata: {device.metadata}")
                    print(f"\tRSSI: {device.rssi}")
                    print(f"\tDistance: {get_distance(device.rssi)}")
                    print('\tServices:')
                    for service in client.services:
                        print(f'\t\tDescription: {service.description}')
                        print(f'\t\tService: {service}')
                        print('\t\tCharacteristics:')
                        for c in service.characteristics:
                            print(f'\t\t\tUUID: {c.uuid}'),
                            print(f'\t\t\tDescription: {c.uuid}')
                            print(f'\t\t\tHandle: {c.uuid}'),
                            print(f'\t\t\tProperties: {c.uuid}')
                            print()
                            print('\t\tDescriptors:')
                            for descriptor in c.descriptors:
                                print(f'\t\t\t{descriptor}')
            except Exception as e:
                print(f"Could not connect to device with info: {device}")
                print(f"Error: {e}")


asyncio.run(main())
