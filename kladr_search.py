import requests
import json

def main(adress):
    a = requests.get('http://localhost:5000/api/v1/Kladr/', params={'adress':adress})
    b = json.loads(a.text)
    return b

if __name__ == "__main__":
    main('мая 1')