import time
import json
from datetime import date
from pprint import pprint

from selenium import webdriver


def parse_data(ip: str):
    driver = webdriver.Chrome()

    login_page = f'http://192.168.1.{ip}/#/login'

    driver.get(login_page)

    login = 'admin'
    password = 'n.123456'

    # fill login form
    username_element = driver.find_element('id', 'username')
    username_element.send_keys(login)

    password_element = driver.find_element('id', 'password')
    password_element.send_keys(password)

    login_btn = driver.find_element('css selector', 'button.login-btn')
    login_btn.click()

    # wait for login
    print('login success')

    # go to event search page
    data_table = f'http://192.168.1.{ip}/#/home/eventSearch'
    driver.get(data_table)
    time.sleep(10)
    print('data_table')

    # get data from table
    list_data = []

    # get page items total
    total_data = driver.find_element('css selector', 'div.page-total.left').text
    total_data = total_data.split(' ')[1]
    print('total_data', total_data)

    # count pages 24 items per page
    pages = int(total_data) // 24
    print('pages', pages)

    # go to next page
    for page in range(pages + 1):
        print('next page', page + 1)

        if page > 0:
            next_page = driver.find_element('css selector', 'span[title="Next Page"]')
            next_page.click()
            time.sleep(10)

        # get data from table
        table_data = driver.find_elements('css selector', 'tr')
        # print('table_data', len(table_data))
        print('---')

        for data_info in table_data[1:-1]:
            data = data_info.text.split('\n')
            # print('data', data)

            # ['00000011 Norqulov Xurshid Authenticated via Face 2024-05-01 05:38:12 08:00']
            device_data = data[0].split(' ')
            # print('device_data', device_data)
            # print('---')

            # ['00000011', 'Norqulov', 'Xurshid', 'Authenticated', 'via', 'Face', '2024-05-01', '05:38:12', '08:00']
            if len(device_data) == 9 and device_data[3] == 'Authenticated':
                # print('check', device_data)
                info = {
                    'device_id': device_data[0],
                    'name': device_data[1] + ' ' + device_data[2],
                    'date': device_data[6],
                    'time': device_data[7]
                }
                list_data.append(info)
                print('info', info)

    pprint(list_data)
    print('---' * 10)

    # save data to file in json
    print('saving data')
    if ip == '188':
        name = f'in_data_{date.today()}.json'
    elif ip == '189':
        name = f'out_data_{date.today()}.json'
    else:
        name = f'data_{date.today()}.json'

    with open(f'data/{name}', 'w') as file:
        json.dump(list_data, file, indent=4)

    print(f'data saved to {name}')

    # close driver
    driver.quit()


if __name__ == '__main__':
    # parse_data('190')
    parse_data('191')