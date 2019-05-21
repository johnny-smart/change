import csv
import string

houses = []
hardware=[]
result=[]

with open('houses.csv', newline='') as houses_read:
    houses_list = csv.reader(houses_read, delimiter=';', quotechar='|')
    
    for row in houses_list:
        houses.append(row)
            
with open('hardware_ku.csv', newline='') as hardware_read:
    hardware_list = csv.reader(hardware_read, delimiter=';', quotechar='|')
    
    for row in hardware_list:
        hardware.append(row)

    for init in hardware:
        street_hard = init[0].lower()
        try:
            number_hard = int(init[1])
        except BaseException:
            number_hard=0        
        for val in houses:
            street_house = val[2].lower()
            try:
                number_house = int(val[3])
            except BaseException:
                number_house=0 
            if((street_house.find(street_hard,0)!=-1)&(number_hard==number_house)):
                result.append(init)
                result.append(val)

    for row in result:
        print(row)    
'''
'''