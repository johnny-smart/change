import xlrd
import xlwt
import csv


def houses_init():  # функция для создания и заполнения массива записей домов
                    # (ввод: имя внутри функции, вывод: маcсив записей)
    houses = []
    '''with open('houses.csv', newline='') as houses_read:  # чтение csv файла
        next(houses_read, None)
        houses_list = csv.reader(houses_read, delimiter=';')

        for row in houses_list:  # заполнение массива данных
            pass
            houses.append(row)
    houses_read.close()'''

    houses_read = xlrd.open_workbook('houses.xlsx')
    house_list = houses_read.sheet_by_index(0)

    for row in range(house_list.nrows):
        houses.append(house_list.row_values(row))

    houses.pop(0)

    return(houses)


def hardware_init(fname):
    hardware = []
    '''
    with open(fname, newline='') as hardware_read:
        next(hardware_read, None)
        hardware_list = csv.reader(hardware_read, delimiter=';')

        for row in hardware_list:
            hardware.append(row)
    '''
    hardware_read = xlrd.open_workbook(fname)
    hardware_list = hardware_read.sheet_by_index(0)

    for row in range(hardware_list.nrows):
        # for row in hardware_list.get_rows():
        hardware.append(hardware_list.row_values(row))
        # hardware.append(row)

    hardware.pop(0)

    return(hardware)


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
                res_tmp.append(init[:4]+row[:4]+[number_hard, number_house])

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


def main():

    houses = houses_init()

    r = result_init(houses, 'Г. КУРОВСКОЕ', 'hardware_ku.xlsx')
    out_file(r)

    r = result_init(houses, 'Г. ЛИКИНО-ДУЛЕВО', 'hardware_ld.xlsx')
    out_file(r)

    r = result_init(houses, 'Г. ОРЕХОВО-ЗУЕВО', 'hardware_oz.xlsx')
    out_file(r)

    # out_console(r)
pass

if __name__ == "__main__":
    main()
