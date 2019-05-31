import openpyxl
import csv
from profilehooks import timecall


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
            if ((init.column == 2) and (init.font.strike == True)):
                cols[19] = 1
            elif (init.column == 2):
                cols[19] = 0
        hardware.append(cols)
    return(hardware)


@timecall
def result_init(houses, town, fname):
    hardware = hardware_init(fname)
    result = []
    print("hardware:", len(hardware))
    for init in hardware:
        res_tmp = []
        try:
            init[2] = ((str(init[2]).split(','))[0].split('.'))[0]
        except BaseException:
            pass

        street_hard = init[1]
        number_hard = init[2]

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

            if((street_house.lower().find(street_hard.lower(), 0) != -1) &
               (number_hard.lower() == number_house.lower()) &
               (row[1] == town)):
                # .append > =
                res_tmp.append(init[:4]+row[:4]+[number_hard, number_house]+[init[19]])

        if not res_tmp:
            # print(init[:4])
            result.append(init)
        else:
            result.append(res_tmp)

    print("result:", len(result))
    return(result)


def out_console(result):
    for row in result:
        print(row)
pass


@timecall
def out_file(result):
    try:
        with open('result.csv', newline='') as newfile:
            scvwr = csv.writer(newfile, delimiter=';')

            for row in result:
                scvwr.writerow(row)
    except BaseException:
        with open('result.csv', 'a+', newline='') as newfile:
            scvwr = csv.writer(newfile, delimiter=';',
                               quoting=csv.QUOTE_MINIMAL)

            scvwr.writerows(result)
        newfile.close()

@timecall
def main():

    houses = houses_init()

    r = result_init(houses, 'Г. КУРОВСКОЕ', 'hardware_ku.xlsx')
    out_file(r)

    r = result_init(houses, 'Г. ЛИКИНО-ДУЛЕВО', 'hardware_ld.xlsx')
    out_file(r)

    r = result_init(houses, 'Г. ОРЕХОВО-ЗУЕВО', 'hardware_oz.xlsx')
    out_file(r)

    #  out_console(r)
pass

if __name__ == "__main__":
    main()
