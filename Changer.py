import csv

houses = []
hardware=[]

with open('houses.csv', newline='') as houses_read:
    houses_list = csv.reader(houses_read, delimiter=';', quotechar='|')
    
    for row in houses_list:
        houses.append(row)
            
with open('hardware_ku.csv', newline='') as hardware_read:
    hardware_list = csv.reader(hardware_read, delimiter=';', quotechar='|')
    
    for row in hardware_list:
        hardware.append(row)

    for init in hardware: 
        print(type(init), init)

'''
'''