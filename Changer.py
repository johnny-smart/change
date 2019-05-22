import csv
import string
i = 0
houses = []
hardware = []
result = []
town = 'Г. КУРОВСКОЕ'
exceptions_result_house = []
exceptions_result_hard = []

with open('houses.csv', newline='') as houses_read:
    houses_list = csv.reader(houses_read, delimiter=';', quotechar='|')
    
    for row in houses_list:
        if(i != 0):
            # row[]
            houses.append(row)
        i = i + 1   

with open('hardware_ku.csv', newline='') as hardware_read:
    hardware_list = csv.reader(hardware_read, delimiter=';', quotechar='|')

    i = 0
    for raw in hardware_list:
        if(i != 0):
            hardware.append(raw)
        i = i + 1

    for init in hardware:
        street_hard = init[0].lower()

        try:
            number_hard = init[1]
        except BaseException:
            number_hard = None       
        

        for val in houses:
            street_house = val[2].lower()

            try:
                # number_house = int(val[3])
                number_house_arr = val[3].split()
                number_house = number_house_arr[0]
              # 
                #    
            except BaseException:
                number_house = "_"

            try:
                if(number_house_arr[1].isalpha()):
                    number_house = number_house_arr[1]
                    number_house_arr[1] = number_house.lower()
                    number_house="".join(number_house_arr)
            except BaseException:
                pass

            if((street_house.find(street_hard,0) != -1) 
                &(number_hard == number_house)
                &(val[1] == town)):
                result.append(init[:3]+val[:4]+[number_hard, number_house] )
            # else:
            #     print("ERR:", init[:3]+val[:4]+[number_hard, number_house])
            

for row in result:
    print (row) 
   
'''
'''