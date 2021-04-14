import api
import sys
import traceback
import random
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
        testi_tapaus("suomi" in random.choice(data)["kieli"], True, True, count, rajapinta)
    except AssertionError as e:
        traceback.print_exc()
        print(e)
        failures += 1
    except IndexError as e:
        print(rajapinta)
    count += 1
    try:
        testi_tapaus("Avoin yo" in random.choice(data)["nimi"], True, False, count, rajapinta)
    except AssertionError as e:
        traceback.print_exc()
        print(e)
        failures += 1
    except IndexError as e:
        print(rajapinta)
    count += 1
    try:
        testi_tapaus("" in random.choice(data)["koulu"], False, True, count, rajapinta)
    except AssertionError as e:
        traceback.print_exc()
        print(e)
        failures += 1
    except IndexError as e:
        print(rajapinta)
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
        print(e)
    count += 1
client = api.app.test_client()
for x  in range(3):
    for i, j in api.rajapinnat.items():
        try:
            test_rajapinta(client, j)
        except Exception as e:
            print(e)
print("Kaikki testit tehty, {} testiä, joista {} ei päässyt läpi".format(count, failures))
        