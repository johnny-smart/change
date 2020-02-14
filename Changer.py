import openpyxl
import csv
import config
from profilehooks import timecall, profile
# from geolocation import geoadressation
from os import remove
from os import path
from err_decorator import error_module
from functools import partial
import json


err_rec = []
# geodata = []


double = []


# функция для создания и заполнения массива записей домов
# (ввод: имя внутри функции, вывод: маcсив записей)
@timecall
def houses_init():
    houses = []
    houses_wb = openpyxl.load_workbook(config.HOUSES)
    houses_sn = houses_wb.sheetnames[0]
    w_sheet = houses_wb[houses_sn]
    houses_list = w_sheet.rows
    next(houses_list)
    for row in houses_list:
        cols = []
        for init in row:
            cols.append(init.value)
        houses.append(cols)
    return(houses)


def houses_filter(town, houses):
    houses_filtred = []
    for row in houses:
        if (row[1] in town):
            houses_filtred.append(row)
    return houses_filtred


@timecall
def hardware_init(fname, sheet):

    hardware = []

    hardware_wb = openpyxl.load_workbook(fname)
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


@timecall
def result_init(houses, arg):
    town, sheet = arg[0], arg[1]
    houses_town = houses_filter(town, houses)
    _err = []
    _double = []
    _result = []

    hardware = hardware_init(config.HARDWARE, sheet)
    print("hardware:", len(hardware))
    for init in hardware:
        res_tmp = []
        try:
            number_hard = ((str(init[1]).split(','))[0].split('.'))[0]
        except BaseException:
            pass

        street_hard = init[0]

        for row in houses_town:

            try:
                number_house_arr = str(row[3]).split()
                row[3] = number_house_arr[0]
                street_house = row[2]
            except BaseException:
                print('err try')

            try:
                if(
                    (number_house_arr[1][0].isalpha()) or
                    ('/' in number_house_arr[1])
                ):
                    row[3] = "".join(number_house_arr)

            except BaseException:
                pass

            number_house = row[3]

            street_hard_tmp = street_hard.upper().strip()

            if ((street_house == 'УЛ. .') or (street_house == 'ул. .') or
               (street_house == 'Ул. .')):
                street_house = row[1]

            if len(street_hard_tmp.split('.')) < 2:
                street_hard_tmp = 'УЛ. ' + street_hard_tmp

            street_house_tmp = street_house.upper().strip()

            if (
                (street_house_tmp == street_hard_tmp) &
                (number_hard.upper().strip() == number_house.upper().strip()) &
                (row[1] in town)
                                ):

                res_tmp.append([init[0]]+[str(init[1])]+init[2:]+[int(row[0])])
                break

        if not res_tmp:

            _err += [init]
        else:
            if (len(res_tmp) > 1):
                for record in res_tmp:
                    if (record[18] or record[19]) == '1':
                        _double += res_tmp
                    else:
                        _result += res_tmp

            else:
                _result += res_tmp


    print("result:", len(_result))
    _result, _err,  = error_module(_result, _err, town)
    return {'result':_result, 'err':_err, 'double':_double}


@timecall
def out_file(result, namefile):
    result = [x for i,x in enumerate(result) if not x is None]


    # try:
    if path.isfile(config.DIR + namefile + '.csv'):
        remove(config.DIR + namefile + '.csv')
    with open(

                config.DIR + namefile + '.csv',
                'a+',
                newline=''

            ) as newfile:

        scvwr = csv.writer(newfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        scvwr.writerows(result)




def regions_worker(reg_list, houses, flag_mod=''):
    _err = []

    _result = [['P_STREET', 'P_HOUSE', 'P_MODEL', 'P_IP_OLD', 'P_IP',
            'P_VECTOR', 'P_UPLINK', 'P_MAC', 'P_VLAN', 'P_DATE_SETUP',
            'P_DATE_INSTALL', 'P_FLATS', 'P_DOOR', 'P_FLOOR',
            'P_DESCRIPTION', 'P_RESERVED1', 'P_RESERVED2', 'P_RESERVED3',
            'P_TRANSIT', 'P_REMOVED', 'P_HOUSE_ID']]

    result_init_tmp = partial(result_init,houses)

    output_init = list(map(result_init_tmp,reg_list))

    for item in output_init:
        _result+=(item['result'])
        _err+=(item['err'])

    for i, d in enumerate(_result):
        if d is None:
            print (i)

    _removed = [x for i,x in enumerate(_err) if x[19] == 1]
    _err = [x for i,x in enumerate(_err) if x[19] is None]

    out_file(_removed, 'Removed' + flag_mod)
    out_file(_result, 'Result' + flag_mod)
    out_file(_err, 'Err' + flag_mod)
    print()


@profile
def main():
    houses = houses_init()

    regions_worker(
        [
            [
                'Д. КАБАНОВО',
                'Комутаторы КБ',
            ],
            [
                'Г. ЛИКИНО-ДУЛЕВО',
                'Комутаторы ЛД',
            ],
            [
                'Г. ОРЕХОВО-ЗУЕВО',
                'Комутаторы ОЗ',
            ],
            [
                'Г. КУРОВСКОЕ',
                'Комутаторы КУ',
            ],
            [
                ['Д. ДЕМИХОВО', 'Д. НАЖИЦЫ', 'Д. КРАСНАЯ ДУБРАВА'],
                'Комутаторы ДМ',
            ],
        ],
        houses
        )


    # regions_worker(
    #     [[
    #             'Г. ОРЕХОВО-ЗУЕВО',
    #             'Комутаторы ОЗ',
    #     ]],
    #     houses,
    #     '_OZ'
    #     )
    print('done')


if __name__ == "__main__":

    main()
