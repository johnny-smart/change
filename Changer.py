import csv
import string

result = []
r = []


def houses_init():
    houses = []
    with open('houses.csv', newline='') as houses_read:
        next(houses_read, None)
        houses_list = csv.reader(houses_read, delimiter=';')
        # i = 0
        for row in houses_list:
            # if(i != 0):
            try:
                # number_house = int(val[3])
                number_house_arr = row[3].split()
                row[3] = number_house_arr[0]
                street_house = row[2].lower()
                row[2] = street_house
            except BaseException:
                number_house = "_"

            try:
                # tra-la-la
                if(number_house_arr[1].isalpha()):
                    number_house = number_house_arr[1]
                    number_house_arr[1] = number_house.lower()
                    row[3] = "".join(number_house_arr)
            except BaseException:
                pass
            houses.append(row)
    return(houses)


def hardware_init(fname):
    hardware = []
    with open(fname, newline='') as hardware_read:
        next(hardware_read, None)
        hardware_list = csv.reader(hardware_read, delimiter=';')

        # i = 0
        for row in hardware_list:
            # if(i != 0):
            try:
                street_hard = init[0].lower()
                row[0] = street_hard
                number_hard_init = row[1].split()
                number_hard = number_hard_init[0].split('.')
                row[1] = number_hard[0]
            except BaseException:
                number_hard = None
            hardware.append(row)
            # i += 1

    return(hardware)


def result_init(houses, town, fname):
    hardware = hardware_init(fname)

    for init in hardware:
        street_hard = init[0]
        number_hard = init[1]

        for val in houses:
            street_house = val[2]
            number_house = val[3]

            if((street_house.find(street_hard, 0) != -1) &
               (number_hard == number_house) &
               (val[1] == town)):
                result.append(init[:3]+val[:4]+[number_hard, number_house])

    return(result)


def out(result):

    for row in result:
        print(row)
pass


def out_file(result):



def main():

    houses = houses_init()

    r = result_init(houses, 'Г. КУРОВСКОЕ', 'hardware_ku.csv')

    r = result_init(houses, 'Г. ЛИКИНО-ДУЛЕВО', 'hardware_ld.csv')

    out(r)
    out_file(r)
pass

if __name__ == "__main__":
    main()
