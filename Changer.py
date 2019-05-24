import csv
import string

houses = []
hardware = []
result = []


def main(fname, town):
    """
    """
    with open('houses.csv', newline='') as houses_read:
        houses_list = csv.reader(houses_read, delimiter=';', quotechar='|')

        i = 0
        for row in houses_list:
            if(i != 0):
                try:
                    # number_house = int(val[3])
                    number_house_arr = row[3].split()
                    row[3] = number_house_arr[0]
                    street_house = row[2].lower()
                    row[2] = street_house
                except BaseException:
                    number_house = "_"

                try:
                    if(number_house_arr[1].isalpha()):
                        number_house = number_house_arr[1]
                        number_house_arr[1] = number_house.lower()
                        row[3] = "".join(number_house_arr)
                except BaseException:
                    pass
                houses.append(row)
            i += 1

    with open(fname, newline='') as hardware_read:
        hardware_list = csv.reader(hardware_read, delimiter=';', quotechar='|')

        i = 0
        for row in hardware_list:
            if(i != 0):
                try:
                    street_hard = row[0].lower()
                    row[0] = street_hard
                    number_hard_init = row[1].split()
                    number_hard = number_hard_init[0].split('.')
                    row[1] = number_hard[0]
                except BaseException:
                    number_hard = None
                hardware.append(row)
            i += 1

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

    for row in result:
        print(row)
pass

if __name__ == "__main__":
    main('hardware_ku.csv', 'Г. КУРОВСКОЕ')
    main('hardware_ld.csv', 'Г. ЛИКИНО-ДУЛЕВО')
