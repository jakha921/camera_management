import json

from datetime import date
from pprint import pprint


# def sort_data(ip: str):
#     # get file name
#     name = f'in_data_{date.today()}.json' if ip == '188' else f'out_data_{date.today()}.json'
#
#     # open file and read data
#     print('sorting data')
#     with open(f'data/{name}', 'r') as file:
#         data = json.load(file)
#
#         # get data from file and filter data by device_id and save to dict
#         list_data = {}
#
#         # get date 188 else data reverse
#         for item in data if ip == '188' else reversed(data):
#             if item['device_id'] not in list_data:
#                 list_data[item['device_id']] = []
#
#             if len(list_data[item['device_id']]) < 1:
#                 list_data[item['device_id']].append(item)
#
#         # convert dict to list
#         data = []
#         for key, value in list_data.items():
#             data.append(value[0])
#
#         # pprint(data)
#
#         # save data to file
#         print('saving sorted data')
#         filter_name = f'in_filter_{date.today()}.json' if ip == '188' else f'out_filter_{date.today()}.json'
#         with open(f'data/{filter_name}', 'w') as filter_file:
#             json.dump(data, filter_file, indent=4)
#
#         print(f'data saved to {filter_name}')
#         print('---' * 10)
#
#         # return path
#         return f'data/{filter_name}'

def get_file_name(ip: str, file_type: str) -> str:
    prefix = "in" if ip == "188" else "out"
    return f"data/{prefix}_{file_type}_{date.today()}.json"


def load_data(file_path: str) -> list:
    with open(file_path, 'r') as file:
        return json.load(file)


def filter_data(data: list, ip: str) -> list:
    list_data = {}
    iterable_data = data if ip == "188" else reversed(data)

    for item in iterable_data:
        if item['device_id'] not in list_data:
            list_data[item['device_id']] = []
        if len(list_data[item['device_id']]) < 1:
            list_data[item['device_id']].append(item)

    return [value[0] for value in list_data.values()]


def save_data(file_path: str, data: list):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {file_path}")


def sort_data(ip: str) -> str:
    input_file = get_file_name(ip, "data")
    print("Sorting data...")
    data = load_data(input_file)
    filtered_data = filter_data(data, ip)
    output_file = get_file_name(ip, "filter")
    save_data(output_file, filtered_data)
    print("---" * 10)
    return output_file


if __name__ == "__main__":
    # Example usage
    ip_address = "188"  # or "189"
    output_path = sort_data(ip_address)
    print(f"Filtered data saved at: {output_path}")
