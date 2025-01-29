import json
import time
from datetime import datetime

from attendance.models import Attendance
from data_parser import parse_data
from scripts.data_filter import sort_data


# def get_data(ip: str):
#     parse_data(ip)
#     path = sort_data(ip)
#
#     time.sleep(10)
#
#     with open(path, 'r') as file:
#         data = json.load(file)
#         return data
#
#
# def put_data_to_db():
#     try:
#         # if now is < 12 pm get ip = 188 else get ip = 189
#         now = datetime.now()
#         print('now', now)
#         if now.hour < 13:
#             ip = '188'
#         else:
#             ip = '189'
#
#         print('ip', ip)
#         data = get_data(ip)
#         for item in data:
#             # if 09:03:00 < time < 18:00:00 then green else red
#             if item['time'] > '09:03:00' and item['time'] < '18:00:00':
#                 item['status_color'] = 'red'
#             else:
#                 item['status_color'] = 'green'
#
#             print('item', item)
#
#             Attendance.objects.create(
#                 name=item['name'],
#                 pinfl=item['pinfl'],
#                 date=item['date'],
#                 time=item['time'],
#                 device_id=item['device_id'],
#                 status_color=item['status_color'],
#                 is_in=True if ip == '188' else False
#             )
#
#             # remove file
#             # os.remove(path)
#
#
#     except Exception as e:
#         # type of error is not important
#         print('error', e)


def get_data(ip: str) -> list:
    """
    Parses and filters data based on the given IP address.

    Args:
        ip (str): IP address ('188' for incoming, '189' for outgoing).

    Returns:
        list: Filtered data as a list of dictionaries.
    """
    parse_data(ip)
    path = sort_data(ip)

    time.sleep(10)  # Allow time for file creation if needed

    with open(path, 'r') as file:
        return json.load(file)


def determine_status_color(time_str: str) -> str:
    """
    Determines the status color based on the time of an event.

    Args:
        time_str (str): Time in 'HH:MM:SS' format.

    Returns:
        str: 'red' if time is between 09:03:00 and 18:00:00, otherwise 'green'.
    """
    return 'red' if '09:03:00' < time_str < '18:00:00' else 'green'


def put_data_to_db():
    """
    Fetches data based on IP and inserts it into the database.
    """
    try:
        now = datetime.now()
        ip = '188' if now.hour < 13 else '189'
        print(f"Current time: {now}, using IP: {ip}")

        data = get_data(ip)
        for item in data:
            item['status_color'] = determine_status_color(item['time'])

            Attendance.objects.create(
                name=item['name'],
                pinfl=item['pinfl'],
                date=item['date'],
                time=item['time'],
                device_id=item['device_id'],
                status_color=item['status_color'],
                is_in=(ip == '188')
            )
            print(f"Inserted: {item}")

    except Exception as e:
        print(f"An error occurred: {e}")


def run_parsing():
    """
    Main function to execute the data parsing and database insertion.
    """
    print("- Start parsing command -")
    put_data_to_db()
    print("- End parsing command -")
