import api
import sys
import traceback
from testitapaus import testi_tapaus
import json
count = 1
failures = 0
def test_rajapinta(client, rajapinta):
    global count
    global failures
    response = client.get(rajapinta)
    data = json.loads(response.get_data().decode(sys.getdefaultencoding()))
    try:
        testi_tapaus(data != None, True, True, count, rajapinta)
    except AssertionError as e:
        failures += 1
        traceback.print_exc()
        print(e)
    count += 1
    try:
        testi_tapaus(type(data) == list, True, True, count, rajapinta)
    except AssertionError as e:
        failures += 1
        traceback.print_exc()
        print(e)
    count += 1
    try:
        testi_tapaus(len(data) > 0, True, True, count, rajapinta)
    except AssertionError as e:
        failures += 1
        traceback.print_exc()
        print(e)
    count += 1
client = api.app.test_client()
for i, j in api.rajapinnat.items():
    test_rajapinta(client, j)
print("Kaikki testit tehty, {} testiä, joista {} ei päässyt läpi".format(count, failures))


        