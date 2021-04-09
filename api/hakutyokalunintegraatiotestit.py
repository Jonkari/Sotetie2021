from opintopolku import opintopolku
from testitapaus import testi_tapaus
count = 0
hakusanat = [
    "monialainen yhteistoiminta",
    "asiakaslähtöi",
    "etiikka",
    "monialaisuu",
    "johtaminen",
    "viestintä",
    "kestävä",
    "laatu",
    "robotiikka",
    "tutkimus",
    "innovaatio",
]
for x in hakusanat:
    data = opintopolku.haeDataa(x)
    for i in data:
        try:
            kurssintiedot = opintopolku.haeKurssinTiedot(i.get('id'))
            testi_tapaus('id' in kurssintiedot, True, True, count, "idtarkistus")
            count += 1
            testi_tapaus('idasdasdasdsa' in kurssintiedot, True, False, count, "vaarakentta")
            count += 1
            testi_tapaus('creditValue' in kurssintiedot and type(kurssintiedot.get('creditValue')) == str, True, True, count, i.get('id'))
            count += 1
        except AssertionError as e:
            print(e)