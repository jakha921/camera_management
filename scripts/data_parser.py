import time
import json
from datetime import date
from pprint import pprint

from selenium import webdriver


# def parse_data(ip: str):
#     driver = webdriver.Chrome()

    # login_page = f'http://192.168.1.{ip}/#/login'
    #
    # driver.get(login_page)
    #
    # login = 'admin'
    # password = 'n.123456'
    #
    # # fill login form
    # username_element = driver.find_element('id', 'username')
    # username_element.send_keys(login)
    #
    # password_element = driver.find_element('id', 'password')
    # password_element.send_keys(password)
    #
    # login_btn = driver.find_element('css selector', 'button.login-btn')
    # login_btn.click()
    #
    # # wait for login
    # print('login success')

    # go to event search page
    # data_table = f'http://192.168.1.{ip}/#/home/eventSearch'
    # driver.get(data_table)
    # time.sleep(10)
    # print('data_table')
    #
    # # get data from table
    # list_data = []
    #
    # # get page items total
    # total_data = driver.find_element('css selector', 'div.page-total.left').text
    # total_data = total_data.split(' ')[1]
    # print('total_data', total_data)
    #
    # # count pages 24 items per page
    # pages = int(total_data) // 24
    # print('pages', pages)

    # go to next page
    # for page in range(pages + 1):
    #     print('next page', page + 1)
    #
    #     if page > 0:
    #         next_page = driver.find_element('css selector', 'span[title="Next Page"]')
    #         next_page.click()
    #         time.sleep(10)
    #
    #     # get data from table
    #     table_data = driver.find_elements('css selector', 'tr')
    #     # print('table_data', len(table_data))
    #     print('---')
    #
    #     for data_info in table_data[1:-1]:
    #         data = data_info.text.split('\n')
    #         # print('data', data)
    #
    #         # ['00000011 Norqulov Xurshid Authenticated via Face 2024-05-01 05:38:12 08:00']
    #         device_data = data[0].split(' ')
    #         # print('device_data', device_data)
    #         # print('---')
    #
    #         # ['00000011', 'Norqulov', 'Xurshid', '32403833960085', 'Authenticated', 'via', 'Face', '2024-05-01', '05:38:12', '08:00']
    #         if len(device_data) == 10 and device_data[4] == 'Authenticated':
    #             # print('check', device_data)
    #             info = {
    #                 'device_id': device_data[0],
    #                 'name': device_data[1] + ' ' + device_data[2],
    #                 'pinfl': device_data[3],
    #                 'date': device_data[7],
    #                 'time': device_data[8]
    #             }
    #             list_data.append(info)
    #             print('info', info)
    #
    # pprint(list_data)
    # print('---' * 10)

    # save data to file in json
    # print('saving data')
    # if ip == '188':
    #     name = f'in_data_{date.today()}.json'
    # elif ip == '189':
    #     name = f'out_data_{date.today()}.json'
    # else:
    #     name = f'data_{date.today()}.json'
    #
    # with open(f'data/{name}', 'w') as file:
    #     json.dump(list_data, file, indent=4)
    #
    # print(f'data saved to {name}')
    #
    # # close driver
    # driver.quit()


def login_to_site(driver, ip: str, username: str, password: str):
    """Handles user login."""
    login_page = f'http://192.168.1.{ip}/#/login'
    driver.get(login_page)

    driver.find_element('id', 'username').send_keys(username)
    driver.find_element('id', 'password').send_keys(password)
    driver.find_element('css selector', 'button.login-btn').click()
    print("Login successful.")


def fetch_data_from_pages(driver, total_pages: int):
    """Fetch data from all pages."""
    all_data = []
    for page in range(total_pages):
        print(f"Fetching page {page + 1}...")
        if page > 0:
            driver.find_element('css selector', 'span[title="Next Page"]').click()
            time.sleep(10)

        rows = driver.find_elements('css selector', 'tr')[1:-1]
        for row in rows:
            # ['00000011 Norqulov Xurshid 32403833960085 Authenticated via Face 2024-05-01 05:38:12 08:00']
            columns = row.text.split('\n')[0].split(' ')

            # ['00000011', 'Norqulov', 'Xurshid', '32403833960085', 'Authenticated', 'via', 'Face', '2024-05-01', '05:38:12', '08:00']
            if len(columns) == 10 and columns[4] == "Authenticated":
                info = {
                    "device_id": columns[0],
                    "name": f"{columns[1]} {columns[2]}",
                    "pinfl": columns[3],
                    "date": columns[7],
                    "time": columns[8]
                }
                print('info', info)
                all_data.append(info)
        print('---' * 10)
    return all_data


def save_data_to_file(data: list, ip: str):
    """Save parsed data to a JSON file."""
    file_prefix = "in" if ip == '188' else "out"
    filename = f"data/{file_prefix}_data_{date.today()}.json"
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}.")


def parse_data(ip: str, username: str = 'admin', password: str = 'n.123456'):
    """Main parser function."""
    driver = webdriver.Chrome()
    try:
        login_to_site(driver, ip, username, password)
        driver.get(f'http://192.168.1.{ip}/#/home/eventSearch')
        time.sleep(10)

        total_items = int(driver.find_element('css selector', 'div.page-total.left').text.split(' ')[1])
        total_pages = -(-total_items // 24)  # Ceiling division
        print(f"Total pages: {total_pages}.")

        data = fetch_data_from_pages(driver, total_pages)
        save_data_to_file(data, ip)
    finally:
        driver.quit()


if __name__ == '__main__':
    # parse_data('190')
    parse_data('191')