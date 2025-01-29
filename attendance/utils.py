import json
from datetime import datetime


# fill db with data
def fill_employee():
    # get json from employees_data.json
    with open('../scripts/employees_data.json', 'r') as file:
        data = json.load(file)
        print('len', len(data))
        for item in data[:10]:
            print('item', item)

            # data format example

            #     "61806015840030": {
            #         "last_name": "Ziyodullayeva",
            #         "first_name": "Nargiza",
            #         "middle_name": "Ixtiyorovna",
            #         "dob": "18.06.2001",
            #         "position": "Kotiba - ish yurituvchi"
            #     },

            print('---')
            print('name', f"{item['last_name']} {item['first_name']} {item['middle_name']}")
            print('pinfl', item)
            print('dob', datetime.strptime(item['dob'], '%d.%m.%Y'))
            print('description', item['position'])

            # Employee.objects.create(
            #     name=f"{item['last_name']} {item['first_name']} {item['middle_name']}",
            #     pinfl=item,
            #     dob=item['dob'],
            #     description=item['position']
            # )


if __name__ == '__main__':
    fill_employee()
    pass
