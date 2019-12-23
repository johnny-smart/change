import requests
import json
import re


def main(town, address):
    print(town)
    address_number_tmp = re.match(r'^(\d+)', address[1]).group(0)
    address_street_tmp = address[0].split('. ')

    if len(address_street_tmp) == 1:
        address_street_tmp.append('ул')
        address_street_tmp.reverse()

    request = requests.get(
        'http://localhost:5000/api/v1/Kladr/',
        params={'adress': " ".join([address[0],address_number_tmp])})
    if request.ok:
        response = json.loads(request.text)
        res = response.get('result')
        if res:
            for item_kladr in res:
                if item_kladr.get('contentType') == 'building':
                    item_kladr = format_kladr(item_kladr)

                    if (address_street_tmp[1].lower() == item_kladr[0].lower()
                                and address[1].lower() == item_kladr[1].lower()
                                and address_street_tmp[0].lower() == item_kladr[2]):

                        return [True, address]
    return [False, address]





def format_kladr(item):
    for parent in item.get('parents'):
        if parent.get('contentType') == 'street':
            return [parent.get('name'), format_item_addr(item.get('name')), parent.get('typeShort') ]


def format_item_addr(addr):
    addr = addr.split(" корпус ")

    if len(addr) == 1:
        addr = addr[0].split(" строение ")

    if len(addr)>1 :
        print(addr)
        if addr[1].isdigit():
           addr =  '/'.join(addr)

    if type(addr) != "string":
        addr = ''.join(addr)

    return addr


if __name__ == "__main__":
    main('Орехово-Зуево',['мая','21е'])