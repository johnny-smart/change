import openpyxl
import csv
import config
from profilehooks import timecall, profile
# from geolocation import geoadressation
from os import remove
from os import path
from err_decorator import error_module
import json
from functools import partial

def main():
    sheet_arr = [
                'Комутаторы ОЗ',

                'Комутаторы ЛД',

                'Комутаторы КУ',
                'Комутаторы КБ',


                'Комутаторы ДМ',
    ]

    hardware_tmp =list(map(hardware_init, sheet_arr))

    hardware = []

    for sheet in hardware_tmp:
        hardware.extend(sheet)

    return hardware


def hardware_init(sheet):
    hardware = []

    hardware_wb = openpyxl.load_workbook(config.HARDWARE)
    hardware_list = hardware_wb[sheet].rows

    next(hardware_list)

    for row in hardware_list:
        cols = [None]*20
        for init in row:
            cols[init.column-1] = init.value

            if (((init.column == 10) or (init.column == 11)) and
               (init.value is not None)):
                cols[init.column-1] = str(init.value).split(' ')[0]
            if (((init.column == 1) or (init.column == 2)) and (init.font.strike is True)):
                cols[19] = 1
            if (init.column == 4 or init.column == 5):
                if(init.fill.fgColor.rgb == 'FF00B0F0'):
                    cols[18] = 1
        if not (cols[0] is None):
            hardware.append(cols)
    return(hardware)


def output_xl_file(hard):
    for i, d in enumerate(hard):
        if d is None:
            print (i)

    if path.isfile(config.DIR + 'hardware_copy_all' + '.csv'):
        remove(config.DIR + 'hardware_copy_all' + '.csv')

    with open(config.DIR + 'hardware_copy_all' + '.csv', 'a+', newline='') as newfile:

        scvwr = csv.writer(newfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        scvwr.writerows(hard)

    print('hardware_copy_all done')
    newfile.close()


def finder(namelist,namespace):
    not_found = {}
    found = {}
    cleared_namespaced = namespace.copy()
    iter_arr = []

    for dev in namelist:
        for i, place in enumerate(namespace.copy()):
            if len(place) != 0:
                if (not place[3] is None):
                    if  not( isinstance(place[3],list)):
                        if place[3].find(';') != -1:
                            place[3] = place[3].split(';')
                        else:
                            place[3] = [place[3]]
                else:
                    place[3] = [place[3]]

                if (not place[4] is None):
                    if not(isinstance(place[4],list)):
                        if place[4].find(';') != -1:
                            place[4] = place[4].split(';')
                        else:
                            place[4] = [place[4]]
                else:
                    place[4] = [place[4]]

                hard_ip = []
                hard_ip.extend(place[4])
                hard_ip.extend(place[3])
                print(hard_ip)
                if dev in hard_ip:
                    found.update({dev:{dev:namelist[dev],'hardware': place}})
                    iter_arr.append(i)
                    break
        else:
            not_found.update({dev:namelist[dev]})

    iter_arr = reversed(sorted(set(iter_arr)))

    for i in iter_arr:
        cleared_namespaced.pop(i)

    return found, not_found, cleared_namespaced


def sort_smart_map(smart_map):
    result = {}
    for row in smart_map:
        result.update({smart_map[row].get('address'): smart_map[row]})
    return result

def output(name, obj):
    if path.isfile(config.DIR + name + '.json'):
        remove(config.DIR + name + '.json')

    with open(config.DIR + name + '.json', 'a+', newline='') as newfile:
        json.dump(obj,newfile)
    pass




if __name__ == "__main__":

    with open(config.PATH_FILTER_XML, 'r', encoding='utf-8-sig') as loaded_map:
        smart_map = json.load(loaded_map)
        smart_map = sort_smart_map(smart_map)

    hard = main()

    hardware = [unit for i, unit in enumerate(hard) if unit[19] != 1]
    hard = {'{}'.format(i): x for i,x in enumerate(hard)}
    len_hard = len(hard)

    found, not_found, excel_not_found = finder(smart_map,hardware)

    output('excel_not_found', excel_not_found)
    print("Всего на карте", len(smart_map))
    print('found',len(found))
    print('active',len(hardware))
    print('hardware', len(hard))
    print('Не найдено в excel active из карты', len(excel_not_found))
    output('map_not_found', list(not_found.keys()) )
    print(not_found.keys())