from datetime import datetime
import time
import json

from attendance.models import Attendance

from filter_data import sort_data
from parser_data import parse_data


def get_data(ip: str):
    parse_data(ip)
    path = sort_data(ip)

    time.sleep(10)

    with open(path, 'r') as file:
        data = json.load(file)
        return data


def put_data_to_db():
    try:
        # if now is < 12 pm get ip = 188 else get ip = 189
        now = datetime.now()
        print('now', now)
        if now.hour < 13:
            ip = '188'
        else:
            ip = '189'

        print('ip', ip)
        data = get_data(ip)
        for item in data:
            # if 09:03:00 < time < 18:00:00 then green else red
            if item['time'] > '09:03:00' and item['time'] < '18:00:00':
                item['status_color'] = 'red'
            else:
                item['status_color'] = 'green'

            print('item', item)

            Attendance.objects.create(
                name=item['name'],
                pinfl=item['pinfl'],
                date=item['date'],
                time=item['time'],
                device_id=item['device_id'],
                status_color=item['status_color'],
                is_in=True if ip == '188' else False
            )

            # remove file
            # os.remove(path)


    except Exception as e:
        # type of error is not important
        print('error', e)


def run_parsing():
    put_data_to_db()
