import json

from datetime import date
from pprint import pprint


def sort_data(ip: str):
    # get file name
    name = f'in_data_{date.today()}.json' if ip == '188' else f'out_data_{date.today()}.json'

    # open file and read data
    print('sorting data')
    with open(f'data/{name}', 'r') as file:
        data = json.load(file)

        # get data from file and filter data by device_id and save to dict
        list_data = {}

        # get date 188 else data reverse
        for item in data if ip == '188' else reversed(data):
            if item['device_id'] not in list_data:
                list_data[item['device_id']] = []

            if len(list_data[item['device_id']]) < 1:
                list_data[item['device_id']].append(item)

        # convert dict to list
        data = []
        for key, value in list_data.items():
            data.append(value[0])

        # pprint(data)

        # save data to file
        print('saving sorted data')
        filter_name = f'in_filter_{date.today()}.json' if ip == '188' else f'out_filter_{date.today()}.json'
        with open(f'data/{filter_name}', 'w') as filter_file:
            json.dump(data, filter_file, indent=4)

        print(f'data saved to {filter_name}')
        print('---' * 10)

        # return path
        return f'data/{filter_name}'


if __name__ == '__main__':
    foo = sort_data()
    print(foo)
