import openpyxl
import csv
from profilehooks import timecall, profile
from geolocation import geoadressation
from os import remove as delite
from os import path
ErrRec = []
geodata = []
result = []
double = []


@timecall
def houses_init():  # функция для создания и заполнения массива записей домов
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
        houses.append(cols)
    # print (w_sheet['B2'].value)
    return(houses)


@timecall
def hardware_init(fname):
    hardware = []
    hardware_wb = openpyxl.load_workbook(fname)
    hardware_sn = hardware_wb.sheetnames[0]
    w_sheet = hardware_wb[hardware_sn]
    hardware_list = w_sheet.rows
    next(hardware_list)
    for row in hardware_list:
        cols = [None]*20
        for init in row:
            cols[init.column-1] = init.value
            if ((init.column == 2) and (init.font.strike is True)):
                cols[19] = 1
            elif (init.column == 2):
                cols[19] = 0
        hardware.append(cols)
    return(hardware)


@timecall
def result_init(houses, town, fname):
    hardware = hardware_init(fname)
    print("hardware:", len(hardware))
    for init in hardware:
        res_tmp = []
        try:
            init[1] = ((str(init[1]).split(','))[0].split('.'))[0]
        except BaseException:
            pass

        street_hard = init[0]
        number_hard = init[1]

        for row in houses:

            try:
                number_house_arr = row[3].split()
                row[3] = number_house_arr[0]
                street_house = row[2]
                row[2] = street_house
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
            if((street_house.find(street_hard, 0) != -1) &
               (number_hard == number_house) &
               (row[1] == town)):
                # .append > =
                res_tmp.append(init[:3]+row[:4]+[number_hard, number_house] +
                                   [init[19]])

        if not res_tmp:
            # print(init[:4])
            ErrRec.append(init)
        else:
            if (len(res_tmp) > 1):
                double.append(res_tmp)
                # print(type(res_tmp[1]))
            else:
                result.append(res_tmp)

            # adress = (res_tmp[0][5] + ', ' + res_tmp[0][1] + ', ' +
            #           res_tmp[0][2])

            # location = geoadressation(adress)
            # geodata.append([str(res_tmp[0][4])] + [location])

    print("result:", len(result))
    return(result)


def out_console(result):
    for row in result:
        print(row)
pass


@timecall
def out_file(result, namefile):
    # try:
    #     with open(namefile + '.csv', newline='') as newfile:
    #         scvwr = csv.writer(newfile, delimiter=';')
    #         for row in result:
    #             scvwr.writerow(row)
    # except BaseException:

    if path.isfile(namefile + '.csv'):
        delite(namefile + '.csv')
    with open(namefile + '.csv', 'a+', newline='') as newfile:
        scvwr = csv.writer(newfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        scvwr.writerows(result)
    newfile.close()


@profile
def main():

    houses = houses_init()

    r = result_init(houses, 'Г. КУРОВСКОЕ', 'hardware_ku.xlsx')
    r = result_init(houses, 'Г. ЛИКИНО-ДУЛЕВО', 'hardware_ld.xlsx')
    r = result_init(houses, 'Г. ОРЕХОВО-ЗУЕВО', 'hardware_oz.xlsx')

    out_file(r, 'result')

    out_file(ErrRec, 'Err')
    out_file(double, 'Дубли')
pass

if __name__ == "__main__":
    main()
