import csv
with open('C:\\Users\\smartintel\\Desktop\\Еремеев\\20190517-data_parser\\houses.csv', newline='') as houses:
    houses_reader = csv.reader(houses, delimiter=';', quotechar='|')
    for row in houses_reader:
        if (row[1] == 'Г. КУРОВСКОЕ'):
            print(type(row), row)
    '''
    
    '''