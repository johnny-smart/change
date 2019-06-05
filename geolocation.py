from geopy.geocoders import Nominatim
from yandex_geocoder import Client
import time


def geoadressation(adress):

    print(adress)

    print("Start : %s" % time.ctime())
    time.sleep(1)
    print("End : %s" % time.ctime())

    def google(adress):
        geolocator = Nominatim(user_agent="my-application")
        location = geolocator.geocode(adress)
        try:
            latitude, longitude = location.latitude, location.longitude
        except BaseException:
            latitude, longitude = 'None', 'None'
        return ('g-' + str(latitude), 'g-' + str(longitude))

    def yandex(adress):
        try:
            location = Client.coordinates(adress)
        except BaseException:
            location = ('None', 'None')
        return location

    _google = ",".join(google(adress))
    _yandex = ",".join(yandex(adress))

    checking = (_google, _yandex)
    checking = "|||".join(checking)

    print(checking)
    print(' ')
    return checking
#geoadressation('Г. КУРОВСКОЕ, Совхозная, 18')