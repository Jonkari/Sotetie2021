from opintopolku import opintopolku
from testitapaus import testi_tapaus
try:
    count = 0
    testi_tapaus(type(opintopolku.haeDataa("testi")), list, True, 1)
    testi_tapaus(len(opintopolku.haeDataa("asdasdasdasdasdasdasdasdasdasda")), 0, True, 2)
    testi_tapaus(len(opintopolku.haeDataa("asdasdasdasdasdasdasdasdasdasda")), 5454, False, 3)
    testi_tapaus(type(opintopolku.haeKurssinTiedot("1.2.246.562.17.63946585526")), dict, True, 4)
    testi_tapaus(type(opintopolku.haeKurssinTiedot("1.2.246.562.17.35717703835")), dict, True, 5)
    testi_tapaus(type(opintopolku.haeKurssinTiedot("1.2.246.562.17.27705333006")), dict, True, 6)
    testi_tapaus(type(opintopolku.haeKurssinTiedot("1.2.246.562.17.33742529283")), dict, True, 7)
    testi_tapaus(type(opintopolku.haeDataa("mitenTääMukaToimii")), list, True, 8)
    testi_tapaus(len(opintopolku.haeDataa("mitäTähänPitäsLaittaa")) > 0, True,  False, 9)
    testi_tapaus(len(opintopolku.haeDataa("asiakaslähtöisyys")), 0, True, 10)
    print("Testejä tehty : {}".format(count))
except AssertionError as e:
    print(e)
