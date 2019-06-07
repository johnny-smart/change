import openpyxl
import csv
from profilehooks import timecall, profile
from geolocation import geoadressation
from os import remove
from os import path


@timecall
def houses_init(town):  # функция для создания и заполнения массива записей домов
                    # (ввод: имя внутри функции, вывод: маcсив записей)
    houses = []
    houses_wb = openpyxl.load_workbook('houses.xlsx')
    houses_sn = houses_wb.sheetnames[0]
    w_sheet = houses_wb[houses_sn]
    houses_list = w_sheet.rows
    next(houses_list)
    for row in houses_list:
        cols = []
        for init in row:
            cols.append(init.value)
        if (cols[1] == town):
            houses.append(cols)
    # print (w_sheet['B2'].value)
    return(houses)


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
            if (init.column == 10) or (init.column == 11):
                cols[init.column-1] = str(init.value).split(' ')[0]
            if ((init.column == 1) and (init.font.strike is True)):
                cols[19] = 1
            if (init.column == 4 or init.column == 5):
                if(init.fill.fgColor.rgb == 'FF00B0F0'):
                    cols[18] = 1

        hardware.append(cols)
    return(hardware)


@timecall
def result_init(town, fname, sheet):
    houses = houses_init(town)
    _err = []
    _double = []
    _result = []

    hardware = hardware_init(fname, sheet)
    print("hardware:", len(hardware))
    for init in hardware:
        res_tmp = []
        try:
            number_hard = ((str(init[1]).split(','))[0].split('.'))[0]
        except BaseException:
            pass

        street_hard = init[0]

        for row in houses:

            try:
                number_house_arr = row[3].split()
                row[3] = number_house_arr[0]
                street_house = row[2]
            except BaseException:
                print('err try')

            try:
                if(number_house_arr[1].isalpha() or
                                              ('/' in number_house_arr[1])):
                    row[3] = "".join(number_house_arr)

            except BaseException:
                pass

            number_house = row[3]

            street_house = street_house.lower().strip()
            street_hard = street_hard.lower().strip()
            number_hard = number_hard.lower().strip()
            number_house = number_house.lower().strip()
            # if((street_house.lower().find(street_hard.lower(), 0) != -1) &
            #    (number_hard.lower() == number_house.lower()) &
            #    (row[1] == town)):
            if (street_house == 'ул. .'):
                street_house = row[1].lower().strip()

            if((street_house.find(street_hard, 0) != -1) &
               (number_hard == number_house) &
               (row[1] == town)):
                # .append > =
                res_tmp.append(init+[int(row[0])])

        if not res_tmp:
            # print(init[:4])
            _err += [init]
        else:
            if (len(res_tmp) > 1):
                _double += res_tmp
                # print(type(res_tmp[1]))
            else:
                _result += res_tmp

            # adress = (res_tmp[0][5] + ', ' + res_tmp[0][1] + ', ' +
            #           res_tmp[0][2])

            # location = geoadressation(adress)
            # geodata.append([str(res_tmp[0][4])] + [location])

    print("result:", len(_result))
    return _result, _double, _err


@timecall
def out_file(result, namefile):
    # try:
    #     with open(namefile + '.csv', newline='') as newfile:
    #         scvwr = csv.writer(newfile, delimiter=';')
    #         for row in result:
    #             scvwr.writerow(row)
    # except BaseException:

    if path.isfile(namefile + '.csv'):
        remove(namefile + '.csv')
    with open(namefile + '.csv', 'a+', newline='') as newfile:
        scvwr = csv.writer(newfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        scvwr.writerows(result)
    newfile.close()


@profile
def main():
    errrec = []
    # geodata = []
    result = [['P_STREET', 'P_HOUSE', 'P_MODEL', 'P_IP_OLD', 'P_IP',
               'P_VECTOR', 'P_UPLINK', 'P_MAC', 'P_VLAN', 'P_DATE_SETUP',
               'P_DATE_INSTALL', 'P_FLATS', 'P_DOOR', 'P_FLOOR',
               'P_DESCRIPTION', 'P_RESERVED1', 'P_RESERVED2', 'P_RESERVED3',
               'P_REMOVED', 'P_TRANSIT', 'P_HOUSE_ID']]
    double = []

    _result, _err, _double = result_init('Г. КУРОВСКОЕ',
                                         'hardware_copy.xlsx',
                                         'Комутаторы КУ')
    result += _result
    errrec += _err
    double += _double

    _result, _err, _double = result_init('Г. ЛИКИНО-ДУЛЕВО',
                                         'hardware_copy.xlsx',
                                         'Комутаторы ЛД')
    result += _result
    errrec += _err
    double += _double

    _result, _err, _double = result_init('Г. ОРЕХОВО-ЗУЕВО',
                                         'hardware_copy.xlsx',
                                         'Комутаторы ОЗ')
    result += _result
    errrec += _err
    double += _double

    _result, _err, _double = result_init('Д. КАБАНОВО',
                                         'hardware_copy.xlsx',
                                         'Комутаторы КБ')
    result += _result
    errrec += _err
    double += _double

    out_file(result, 'result')
    out_file(errrec, 'Err')
    out_file(double, 'Дубли')
pass

if __name__ == "__main__":
    main()


# houses_init :=9):
#     1.341 seconds


#   hardware_init :=28):
#     0.448 seconds

# hardware: 59
# result: 59

#   result_init :=50):
#     1.967 seconds


#   houses_init :=9):
#     1.360 seconds


#   hardware_init :=28):
#     0.449 seconds

# hardware: 155
# result: 155

#   result_init :=50):
#     2.303 seconds


#   houses_init :=9):
#     1.403 seconds


#   hardware_init :=28):
#     0.487 seconds

# hardware: 647
# result: 647

#   result_init :=50):
#     7.461 seconds


#   houses_init :=9):
#     1.491 seconds


#   hardware_init :=28):
#     0.460 seconds

# hardware: 16
# result: 16

#   result_init :=50):
#     1.961 seconds


#   out_file :=123):
#     0.008 seconds


#   out_file :=123):
#     0.001 seconds


#   out_file :=123):
#     0.001 seconds

