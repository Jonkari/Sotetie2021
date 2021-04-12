from opintopolku import opintopolku
from testitapaus import testi_tapaus
try:
    count = 1
    testi_tapaus(type(opintopolku.haeDataa("testi")), list, True, count)
    count += 1
    testi_tapaus(len(opintopolku.haeDataa("asdasdasdasdasdasdasdasdasdasda")), 0, True, count)
    count += 1
    testi_tapaus(len(opintopolku.haeDataa("asdasdasdasdasdasdasdasdasdasda")), 5454, False, count)
    count += 1
    testi_tapaus(type(opintopolku.haeKurssinTiedot("1.2.246.562.17.63946585526")), dict, True, count)
    count += 1
    testi_tapaus(type(opintopolku.haeKurssinTiedot("1.2.246.562.17.35717703835")), dict, True, count)
    count += 1
    testi_tapaus(type(opintopolku.haeKurssinTiedot("1.2.246.562.17.27705333006")), dict, True, count)
    count += 1
    testi_tapaus(type(opintopolku.haeKurssinTiedot("1.2.246.562.17.33742529283")), dict, True, count)
    count += 1
    testi_tapaus(type(opintopolku.haeDataa("mitenTääMukaToimii")), list, True, count)
    count += 1
    testi_tapaus(len(opintopolku.haeDataa("mitäTähänPitäsLaittaa")) > 0, True,  False, count)
    count += 1
    testi_tapaus(len(opintopolku.haeDataa("asiakaslähtöisyys")), 0, True, count)
    count += 1
    print("Testejä tehty : {}".format(count))
except AssertionError as e:
    print(e)
