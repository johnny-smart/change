import csv
import string


def houses_init():  # функция для создания и заполнения массива записей домов
                    # (ввод: имя внутри функции, вывод: маcсив записей)
    houses = []
    with open('houses.csv', newline='') as houses_read:  # чтение csv файла
        next(houses_read, None)
        houses_list = csv.reader(houses_read, delimiter=';')

        for row in houses_list:  # заполнение массива данных
            pass
            houses.append(row)
    houses_read.close()
    return(houses)


def hardware_init(fname):
    hardware = []

    with open(fname, newline='') as hardware_read:
        next(hardware_read, None)
        hardware_list = csv.reader(hardware_read, delimiter=';')

        for row in hardware_list:
            hardware.append(row)
    hardware_read.close()
    return(hardware)


def result_init(houses, town, fname):
    hardware = hardware_init(fname)
    result = []
    print("hardware:", len(hardware))
    for init in hardware:
        res_tmp = []
        try:
            street_hard = init[1]
            init[1] = street_hard
            number_hard_init = init[2].split(',')
            number_hard = number_hard_init[0].split('.')
            init[2] = number_hard[0]
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
                if(number_house_arr[1].isalpha()):
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

    r = result_init(houses, 'Г. КУРОВСКОЕ', 'hardware_ku.csv')
    out_file(r)

    r = result_init(houses, 'Г. ЛИКИНО-ДУЛЕВО', 'hardware_ld.csv')
    out_file(r)

    r = result_init(houses, 'Г. ОРЕХОВО-ЗУЕВО', 'hardware_oz.csv')
    out_file(r)

    # out_console(r)
pass

if __name__ == "__main__":
    main()
