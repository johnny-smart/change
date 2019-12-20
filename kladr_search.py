import requests
import json
import re


def main(address):
    address_tmp = re.match(r'^(\d+)', address[1]).group(0)
    request = requests.get(
        'http://localhost:5000/api/v1/Kladr/',
        params={'adress': " ".join([address[0],address_tmp])})
    if request.ok:
        response = json.loads(request.text)
        res = response.get('result')
        if res:
            for item in res:
                if item.get('contentType') == 'building':
                    item = format_kladr(item)
                    if address[0].lower() == item[0].lower() and address[1].lower() == item[1].lower():
                        return [True, address]
    return [False, address]


def format_kladr(item):
    for parent in item.get('parents'):
        if parent.get('contentType') == 'street':
            return [parent.get('name'), format_item_addr(item.get('name'))]


def format_item_addr(addr):
    addr = re.sub(r' корпус ','',addr)
    addr = re.sub(r'')
    # re.sub(r' строение ','/',addr)
    return addr


if __name__ == "__main__":
    main(['мая','21е'])