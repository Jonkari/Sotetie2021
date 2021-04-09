import api
import sys
from testitapaus import testi_tapaus
import json
def test_rajapinta(client, rajapinta, count):
    response = client.get(rajapinta)
    data = json.loads(response.get_data().decode(sys.getdefaultencoding()))
    
    testi_tapaus(data != None, True, True, count)
    count += 1
    testi_tapaus(type(data) == list, True, True, count)
    count += 1
client = api.app.test_client()
count = 1
for i, j in api.rajapinnat.items():
    test_rajapinta(client, j, count)
print("Kaikki testit tehty")


        