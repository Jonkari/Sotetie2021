import requests
import json
from kurssi import Kurssi
HEADERS = {"Caller-Id":"JokuStringivaa"}
objs = []
def haeDataa(hakusanat,hakutyyppi="ongoing"):
    """Haku opintopolusta

    Args:
        hakusanat (string): Hakusanat opintopolku API rajapintaan
        hakutyyppi (string): Tähän tulee arvot [ongoing], [upcoming] tai [upcomingLater], vakiona ongoing

    Returns:
        dict: Palauttaa Python Dictionaryn, jonka kanssa voi työskennellä
    """
    #Hak
    hakusanat = requests.utils.quote(hakusanat)
    data = requests.get('https://opintopolku.fi/lo/search?start=0&rows=25000&lang=fi&searchType=LO&text={hakusanat}&{hakutyyppi}=true'
    .format(
        hakusanat=hakusanat,
        hakutyyppi=hakutyyppi
    )
    , headers=HEADERS)
    return data.json().get("results")
def haeKurssinTiedot(kurssin_id):
    """Hakee kurssin tiedot

    Args:
        kurssin_id (string): Kurssin tunnus

    Returns:
        dict: Palauttaa kurssin tiedot
    """
    data = requests.get('https://opintopolku.fi/lo/koulutus/{kurssin_id}'
    .format(kurssin_id=kurssin_id)
    , headers=HEADERS)
    return data.json()
def luoKurssiObjektit(data):
    print(len(data))
    for i in data:
        if i.get('id') is not None:
            kurssi_data = haeKurssinTiedot(i.get('id'))
            kurssi_obj = Kurssi(
                kurssi_data.get('name'),
                kurssi_data.get('creditValue'),
                kurssi_data.get('content') or kurssi_data.get('opetuksenAikaJaPaikka') or kurssi_data.get('lisatietoja'),
                kurssi_data.get('provider').get('name'),
                kurssi_data.get('provider').get('visitingAddress') or kurssi_data.get('provider').get('postalAddress'),
                kurssi_data.get('id'),
                kurssi_data.get('formOfTeaching') or kurssi_data.get('teachingPlaces'),
                kurssi_data.get('availableTranslationLanguages'),
                kurssi_data.get('applicationSystems')[0].get('applicationDates')[0].get('startDate'),
                kurssi_data.get('applicationSystems')[0].get('applicationDates')[0].get('endDate')
                )
            objs.append(kurssi_obj)
            if kurssi_obj.testaa():
                print("----------------------------------")
luoKurssiObjektit(haeDataa("avoin yo", "ongoing"))
print(objs)
print(objs[0])

print("finished")