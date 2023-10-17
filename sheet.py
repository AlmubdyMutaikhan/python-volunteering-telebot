import random

import gspread
import uuid
import datetime

sa = gspread.service_account(filename='key.json')
sh = sa.open('komekappbot')


def addRow(user):
    wks = sh.worksheet(user.city)
    #TODO: Add validation rules
    order = []
    order_id = str(uuid.uuid4())
    order.append(order_id)
    createdAt = str(datetime.datetime.now())
    order = order + [user.order['desc'], user.order['cat'], user.order['dur'], user.order['loc'], createdAt] + [user.city, user.username, '', user.name]
    print(order)
    try:
        wks.append_row(order)
        print('data added')
        return order_id
    except Exception as inst:
        return ''

def getData(city):
    wks = sh.worksheet(city)
    data = wks.get_all_values()
    data = data[1::]
    random.shuffle(data)
    print('data in array is ', data)
    return data



def addComment(id, city,  rowIndex='I', comment='no commment'):
    wks = sh.worksheet(city)
    try:
        row = wks.find(id)
        rowNumber = rowIndex + str(row._row)
        rowNumberStatus = 'L' + str(row._row)
        wks.update_acell(rowNumber, comment)
        wks.update_acell(rowNumberStatus, 'done')
        return True
    except Exception as inst:
        return False

