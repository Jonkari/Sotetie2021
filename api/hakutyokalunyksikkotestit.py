from opintopolku import opintopolku
from testitapaus import testi_tapaus
try:
    data = opintopolku.haeDataa("etiikka")
    testi_tapaus(type(opintopolku.haeDataa("testi")), list, True, 1)
    testi_tapaus(len(opintopolku.haeDataa("asdasdasdasdasdasdasdasdasdasda")), 0, True, 2)
    testi_tapaus(len(opintopolku.haeDataa("asdasdasdasdasdasdasdasdasdasda")), 5454, False, 3)
    count = 4
    for i in data:
        try:
            kurssintiedot = opintopolku.haeKurssinTiedot(i.get('id'))
            testi_tapaus('id' in kurssintiedot, True, True, count)
            count += 1
            testi_tapaus('idasdasdasdsa' in kurssintiedot, True, False, count)
            count += 1
            testi_tapaus('startDate' in kurssintiedot and type(kurssintiedot.get('startDate')) == int, True, True, count, i.get('id'))
            count += 1
        except AssertionError as e:
            print(e)
    print("Testejä tehty : {}".format(count))
except AssertionError as e:
    print(e)
