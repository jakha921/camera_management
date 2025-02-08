import time
import json
import os
from selenium import webdriver

# Load data from JSON file
with open("emp_data.json", "r", encoding="utf-8") as file:
    people_data = json.load(file)

def parse_data(ip: str):
    errors = []
    driver = webdriver.Chrome()
    driver.get(f'http://192.168.1.{ip}/#/login')

    # Login
    driver.find_element('id', 'username').send_keys('admin')
    driver.find_element('id', 'password').send_keys('n.123456')
    driver.find_element('css selector', 'button.login-btn').click()
    driver.save_screenshot("./screenshot.png")
    print('login success')

    # Navigate to people management page
    driver.get(f'http://192.168.1.{ip}/index.asp#/home/peopleManage')
    time.sleep(3)

    for index, person in enumerate(people_data):
        print(f'Processing person {index + 1} of {len(people_data)}: {person["first_name"]} {person["last_name"]}')

        try:
            # Open "Add Person" modal for each person
            driver.find_element('css selector', 'li[ng-click="peopleManage.showAddEditDlg(\'add\')"]').click()
            time.sleep(1)

            # Fill form
            driver.find_element('css selector', 'input[ng-model="oPeopleInfo.szWorkNo"]').send_keys(str(index + 1))
            driver.find_element('css selector', 'input[ng-model="oPeopleInfo.szName"]').send_keys(person['last_name'] + ' ' + person['first_name'])

            if person['image']:
                path = os.path.abspath(os.getcwd()) + '\\'
                driver.find_element('css selector', 'input[type="file"]').send_keys(path + person['image'])
                time.sleep(3)

            # Add card
            driver.find_element('css selector', 'div.add-card').click()
            time.sleep(1)
            driver.find_element('css selector', 'input[ng-model="oCurrentCard.cardNo"]').send_keys(person['pinfl'])

            # Confirm card addition
            btn = driver.find_elements('css selector', 'a.layui-layer-btn0')
            if len(btn) >= 2:
                btn[1].click()
                time.sleep(2)
                btn[0].click()

            print(f'Person with {person["pinfl"]} PINFL added successfully')
            print('---------------------------------')
            time.sleep(3)

        except Exception as e:
            errors.append(person)
            print(f'Error adding person with {person["pinfl"]} PINFL, {e}')
            print('---------------------------------')
            time.sleep(3)

    driver.quit()
    print('end')

if __name__ == '__main__':
    parse_data('190')
