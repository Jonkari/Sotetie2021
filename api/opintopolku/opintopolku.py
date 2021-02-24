import requests
import json
if __name__ == "__main__":
    import kurssi
else:
    from opintopolku import kurssi
HEADERS = {"Caller-Id":"JokuStringivaa"}
objs = {}
def haeDataa(hakusanat, facetFilter="et01.05.03",hakutyyppi="ongoing"):
    """Hakee dataa opintopolku.fi sivustosta

    Args:
        hakusanat (str): Hakusanat, millä haetaan.
        facetFilter (str, optional): Arvot ovat: et01.05.03 (Yliopisto) tai et01.04.03 (AMK)  Defaults to "et01.05.03".
        hakutyyppi (str, optional): Hakutyyppi, mahdolliset arvot ovat ongoing, upcoming ja upcomingLater. Defaults to "ongoing".


    Returns:
        dict: Data, Python Dictionaryna.
    """
    #Hak
    hakusanat = requests.utils.quote(hakusanat)
    data = requests.get('https://opintopolku.fi/lo/search?start=0&rows=25000&lang=fi&searchType=LO&text={hakusanat}&{hakutyyppi}=true&&facetFilters=educationType_ffm:{facetFilter}&facetFilters=theme_ffm:teemat_12'
    .format(
        hakusanat=hakusanat,
        hakutyyppi=hakutyyppi,
        facetFilter=facetFilter
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
def hakuTyokaluYksinkertainen():
    hakusanat_dict = {
        "asiakaslähtoisyys": [
            "asiakaslähtoi",
            "osallisuus",
            "kohtaaminen",
            "palvelutar",
            "asiakasprosessi"
        ],
        "ohjaus- ja neuvontaosaaminen" : [
            "ohjaus",
            "neuvonta",
            "palvelujärjestelmä",
            "vuorovaikutus",
            "kommunikaatio"
        ],
        "palvelujärjestelmät" : [
            "palvelujärjestelmät",
            "palvelujärjestelmä",
            "palveluohjaus",
        ],
        "lainsäädäntö ja etiikka" : [
            "etiikka",
            "lainsäädäntö",
            "tietosuoja",
            "vastuu",
            "eettinen"
        ],
        "tutkimus- ja kehittämisosaaminen" : [
            "tutkimus",
            "innovaatio",
            "kehittäminen"
        ],
        "robotiikka ja digitalisaatio" : [
            "robotiikka",
            "digi",
            "tekoäly",
            "sote-palvelut",
            "tietoturva",
            "tietosuoja",
        ],
        "vaikuttavuus- kustannus- ja laatutietoisuus" : [
            "laatu",
            "laadun",
            "vaikuttavuu",
            "vaikutusten",
            "kustannukset"
        ],
        "kestävän kehityksen osaaminen" : [
            "kestävä",
            "ekolog",
            "kestävyys",
            "kierrätys",
            "ympäristö",
            "energiankulutus"
        ],
        "viestintäosaaminen" : [
            "viestintä",
            "tunnetila",
            "empatia",
            "selkokieli",
            "selko"
        ],
        "työntekijyysosaaminen" : [
            "osaamisen",
            "johtaminen",
            "työhyvinvointi",
            "muutososaaminen",
            "muutosjoustavuus",
            "urakehitys",
            "verkostotyö",
            "työyhteisö",
            "moniammatillisuus"
        ],
        "monialainen yhteistoiminta" : [
            "monialaisuu",
            "moniammatillisuu",
            "monitiet",
            "yhteistyö",
            "verkostoituminen",
            "asiantuntijuus"
        ]
    }
    for facetFilter in ['et01.05.03', 'et01.04.03']:
        for osaaminen, hakusanat in hakusanat_dict.items():
            for hakusana in hakusanat:
                for i in haeDataa(hakusana, facetFilter):
                    kurssi_obj = kurssi.Kurssi(
                        i.get('name'),
                        i.get('credits')[0],
                        i.get('lopNames')[0],
                        i.get('id'),
                        "",
                        osaaminen
                    )
                    if i.get('id') not in objs:
                        objs[i.get('id')] = kurssi_obj
                    else:
                        if osaaminen not in objs[i.get('id')].osaamiset:
                            objs[i.get('id')].osaamiset += "|"+osaaminen
    haeKielet()
def haeKielet():
    for i, j in objs.items():
        data = haeKurssinTiedot(i)
        j.kieli = data.get('teachingLanguages')[0]
if __name__ == "__main__":
    hakuTyokaluYksinkertainen()
    haeKielet()