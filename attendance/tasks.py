from datetime import date, datetime
from unittest import TestCase

from attendance.models import Attendance
from parser_data import parse_data
from filter_data import sort_data
import time
import json


def get_data():

    # if now is < 12 pm get ip = 188 else get ip = 189
    now = datetime.now()
    if now.hour < 12:
        ip = '188'
    else:
        ip = '189'

    parse_data(ip)
    path = sort_data(ip)

    time.sleep(10)

    with open(path, 'r') as file:
        data = json.load(file)
        return data


def put_data_to_db():
    data = get_data()
    for item in data:
        print('item', item)
        # put data to db
        Attendance.objects.create(
            name=item['name'],
            date=item['date'],
            time=item['time'],
            device_id=item['device_id']
        )

        print('data saved')

        # remove file


def run_parsing():
    put_data_to_db()
