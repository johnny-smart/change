import requests
import json
import re
import config_kladr
from functools import partial
import redis
import hashlib
from profilehooks import timecall

redis_connect = redis.StrictRedis(config_kladr.REDIS_HOST,config_kladr.REDIS_PORT, config_kladr.REDIS_DB, config_kladr.REDIS_PASSWORD)

err_tmp = []

# def error_module(_result, _err, town):
#     error_module_fun = partial(main, town)
#     re_search = (list(map(error_module_fun, _err)))

#     print(re_search)
#     _result.extend(re_search)
#     _err = err_tmp
#     return _result, _err


def error_module(_result, town):
    if isinstance(town,list):
        town = town[0]
    error_module_fun = partial(main, town)
    re_search_result = (list(map(error_module_fun, _result)))

    _err = err_tmp.copy()
    err_tmp.clear()
    return re_search_result, _err



def main(town, address):
    if address[19] == 1:
        address.append('REMOVED')
        return err_tmp.append(address)

    reg_code = town_code(town)

    try:
        address_number_tmp = (re.match(r'^(\d+\w+)', address[1]).group(0))
    except BaseException:
        address_number_tmp = (re.match(r'^(\d+)', address[1]).group(0))

    address_street_tmp = address[0].lower().split('. ')

    if len(address_street_tmp) == 1:
        address_street_tmp.append('ул')
        address_street_tmp.reverse()

    try:
        village = re.match(r'^(\w[.])',address[0]).group(0).lower()
        if (village  == 'д.'):
            reg_code = town_code(address[0])
            address_street_tmp = address[0].lower().split('. ')
            street_code = ''
            address_tmp = building(address_number_tmp, street_code, address, reg_code)
            if address_tmp:
                return address_tmp

            try:
                kladr_number = (re.match(r'^(\d+[/]\d)', address[1]).group(0))
            except BaseException:
                kladr_number = (re.match(r'^(\d+)', address[1]).group(0))

            address_tmp = building(address_number_tmp, street_code, address, reg_code, kladr_number)
            if address_tmp:
                return address_tmp

            return err_tmp.append(address)
    except BaseException:
        pass



    hash_redis_street = hashing(address_street_tmp[1].upper(), reg_code)
    get_redis = redis_data_output(address_street_tmp[1], reg_code, hash_redis_street)

    if not get_redis:
        request = requests.get(
            'http://localhost:5000/api/v1/Kladr/street',
            params={'cityId':reg_code,'address':address_street_tmp[1]})

    if get_redis:
        response = json.loads(get_redis)
        resp = response.get('result')
    elif request.ok:
        response = json.loads(request.text)
        resp = response.get('result')

    if resp:
        street_code = compare_kladr(resp, address_street_tmp, reg_code, 'street')

    address_tmp = building(address_number_tmp, street_code, address, reg_code)
    if address_tmp:
        return address_tmp

    try:
        address_number_tmp = (re.match(r'^(\d+[/]\d)', address[1]).group(0))
        kladr_number = (re.match(r'^(\d+)', address[1]).group(0))
    except BaseException:
        kladr_number = (re.match(r'^(\d+)', address[1]).group(0))
    address_tmp = building(address_number_tmp, street_code, address, reg_code, kladr_number)
    if address_tmp:
        return address_tmp

    err_tmp.append(address)


def building(address_number_tmp, street_code, address, reg_code, kladr_number=None):
    if not kladr_number:
        kladr_number = address_number_tmp
    try:
        village = re.match(r'^(\w[.])',address[0]).group(0).lower()
    except BaseException:
        village = ''

    if (street_code) or ( village == 'д.'):
        hash_redis_build = hashing(kladr_number.upper() + street_code, reg_code)
        get_redis_street = redis_data_output(address_number_tmp, street_code, hash_redis_build)

        if not get_redis_street:
            request = requests.get(
                'http://localhost:5000/api/v1/Kladr/building',
                params={'cityId':reg_code,'streetId': street_code,'building': kladr_number}
            )

        if get_redis_street:
            response = json.loads(get_redis_street)
            resp_build = response.get('result')
        elif request.ok:
            response = json.loads(request.text)
            resp_build = response.get('result')

        if street_code == '':
            if (re.match(r'^(\w[.])',address[0]).group(0).lower() == 'д.'):
                street_code = reg_code

        kladr_unit = compare_kladr(resp_build, address_number_tmp, street_code, 'building')
        if kladr_unit:
            address.append(00)
            return address
    return False



def compare_kladr(resp, address_tmp, reg_code, options):
    if options == 'street':
        address_short_prefix = address_tmp[0]
        address_tmp = address_tmp[1].strip()
    if resp:
        for item_kladr in resp:
            if (item_kladr.get('contentType') == options):
                if item_kladr.get('parents'):
                    for parent in item_kladr.get('parents'):
                        if item_kladr.get('parentGuid') == parent.get('guid') and reg_code == parent.get('id'):
                            if (address_tmp.lower() == item_kladr['name'].lower()) or (address_tmp.lower() == format_item_addr(item_kladr['name'].lower())):
                                if (options == 'street') and (item_kladr['typeShort'] == address_short_prefix):
                                    return item_kladr['id']
                                elif options == 'building':
                                    return item_kladr
    return False


def hashing(address, cityId):
    s = ':'.join([address, cityId])
    hash_string = hashlib.sha1(s.encode()).hexdigest()
    return hash_string


# @timecall
def redis_data_output(address, cityId, hashing_string):
    request_data = redis_connect.get(hashing_string)
    redis_connect.pttl(hashing_string)

    if request_data:

        if not(config_kladr.ENV == 'production'):
            print({
                'adress': address,
                'Id': cityId,
                'pttl': redis_connect.pttl(hashing_string)/3600000
                })
    else :
        request_data={}
    return request_data

# def main(town, address):
#     reg_code = town_code(town)
#     address_number_tmp = re.match(r'^(\d+)', address[1]).group(0)
#     address_street_tmp = address[0].split('. ')

#     if len(address_street_tmp) == 1:
#         address_street_tmp.append('ул')
#         address_street_tmp.reverse()

#     request = requests.get(
#         'http://localhost:5000/api/v1/Kladr/',
#         params={'cityId':reg_code,'address': " ".join([address[0],address_number_tmp])})
#     if request.ok:
#         response = json.loads(request.text)
#         res = response.get('result')
#         if res:
#             for item_kladr in res:
#                 if item_kladr.get('contentType') == 'street':
#                     item_kladr = format_kladr(item_kladr)

#                     if (address_street_tmp[1].lower() == item_kladr[0].lower()
#                                 and address[1].lower() == item_kladr[1].lower()
#                                 and address_street_tmp[0].lower() == item_kladr[2]):
#                         address.append('00')
#                         return address
#     return err_tmp.append(address)


def town_code(town):
    if isinstance(town, list):
        town = town[0]

    town = town.split('. ')
    if town[1].upper() in config_kladr.FIAS_CODE:
       return config_kladr.FIAS_CODE.get(town[1].upper())

# def format_kladr(item):
#     for parent in item.get('parents'):
#         if parent.get('contentType') == 'street':
#             return [parent.get('name'), format_item_addr(item.get('name')), parent.get('typeShort') ]


def format_item_addr(addr):
    addr = addr.split(" корпус ")

    if len(addr) == 1:
        addr = addr[0].split(" строение ")

    if len(addr)>1 :
        if addr[1].isdigit():
           addr =  '/'.join(addr)

    if type(addr) != "string":
        addr = ''.join(addr)

    return addr


if __name__ == "__main__":
    # print(main('Г. Орехово-Зуево', ['мая','21']))
    # print(main('Г. Ликино-Дулево', ['Ленина','15/1']))
    print(main('Г. Орехово-Зуево', ['Нажицы','8']))