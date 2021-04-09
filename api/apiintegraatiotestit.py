import api
import sys
from testitapaus import testi_tapaus
import json
def test_rajapinta(client, rajapinta, count):
    response = client.get(rajapinta)
    data = json.loads(response.get_data().decode(sys.getdefaultencoding()))
    try:
        testi_tapaus(data != None, True, True, count, rajapinta)
    except AssertionError as e:
        print(e)
    count += 1
    try:
        testi_tapaus(type(data) == list, True, True, count, rajapinta)
    except AssertionError as e:
        print(e)
    count += 1
    try:
        testi_tapaus(len(data) > 0, True, True, count, rajapinta)
    except AssertionError as e:
        print(e)
    count += 1
client = api.app.test_client()
count = 1
for i, j in api.rajapinnat.items():
    test_rajapinta(client, j, count)
print("Kaikki testit tehty")


        