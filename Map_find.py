from lxml import etree
import json
from agregate import check_changer

def main(map_loc):
    found_types = []
    with open('C:/Project/OUTPUT/Changer/excel_not_found.json', 'r', encoding='utf-8-sig') as json_err:
        not_found_in_map = json.load(json_err)
    with open(map_loc, 'r', encoding='utf-8-sig') as xml_map_reader:
        xml_map = etree.parse(xml_map_reader)

    # devices = xml_map.xpath("/Map/Devices/Device[@address='{0}']".format('10.110.10.4'))

    for item in not_found_in_map:
        if item[4]:
            ip_tmp = item[4]
        else:
            ip_tmp = item[3]
        for ip in ip_tmp:
            devices = xml_map.xpath("/Map/Devices/Device[@address='{0}']/@type-id".format(ip))
            if devices:
                found_types.append({ip:devices})
                break
            
    return found_types

if __name__ == "__main__":
    print(main('C:/Project/OUTPUT/smartintel_new.map'))