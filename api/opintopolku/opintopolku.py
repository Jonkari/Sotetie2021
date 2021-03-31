import requests
import re
import json
from . import kurssi
HEADERS = {"Caller-Id":"JokuStringivaa"}
objs = {}
tmp = {}
def haeDataa(hakusanat, facetFilter="et01.05.03",hakutyyppi="ongoing"):
    """Hakee dataa opintopolku.fi sivustosta

    Args:
        hakusanat (str): Hakusanat, millä haetaan.
        kieli (str): Kieli, millä haetaan.
        facetFilter (str, optional): Arvot ovat: et01.05.03 (Yliopisto) tai et01.04.03 (AMK)  Vakioarvo "et01.05.03".
        hakutyyppi (str, optional): Hakutyyppi, mahdolliset arvot ovat ongoing, upcoming ja upcomingLater. Vakioarvo "ongoing".


    Returns:
        list: Data, Python Listana.
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
    global tmp
    global objs
    """
    Käyttää haeDataa ja haeKielet funktioita ja luo `objs` muuttujaan `Kurssi` objektit, joita käytetään tietokantaan tallentamisen yhteydessä.
    """
    try:
        hakusanat_dict = {
            "asiakaslähtöisyys": {
                "fi" : [
                    "asiakaslähtöi",
                    "osallisuus",
                    "kohtaaminen",
                    "palvelutar",
                    "asiakasprosessi"
                ],
                "se" : [
                    "delaktighet",
                    "klientcentrering",
                    "klientcent",
                    "klientorient",
                    "delaktighet",
                    "bemötande",
                    "serviceutbud",
                    "servicebehov",
                    "klientprocess"
                ],
                "en" : [
                    "customer oriented",
                    "participation",
                    "meeting",
                    "service",
                    "customer process",
                ]
            },
            "ohjaus- ja neuvontaosaaminen" : {
                "fi" : [
                    "ohjaus",
                    "neuvonta",
                    "palvelujärjestelmä",
                    "vuorovaikutus",
                    "kommunikaatio"
                ],
                "se" : [
                    "handleda",
                    "handledning",
                    "handled",
                    "rådgiva",
                    "rådgiv",
                    "servicesystem",
                    "interaktion",
                    "växelverkan",
                    "kommunikation"
                ],
                "en" : [
                    "guidance",
                    "advice",
                    "information",
                    "counseling",
                    "service system",
                    "interaction",
                    "communication",
                ]
            },
            "palvelujärjestelmät" : {
                "fi" : [
                    "palvelujärjestelmät",
                    "palvelujärjestelmä",
                    "palveluohjaus"
                ],
                "se" : [
                    "servicesystem",
                    "servicehandledning",
                    "servicehandl",
                    "information",
                    "rådgivning",
                    "servicenätverk",
                    "serviceproducent",
                ],
                "en" : [
                    "service system",
                    "service guidance",
                    "advice",
                    "service connections",
                    "service network",
                    "service producer",
                ]
            },
            "lainsäädäntö ja etiikka" : {
                "fi" : [
                    "etiikka",
                    "lainsäädäntö",
                    "tietosuoja",
                    "vastuu",
                    "eettinen"
                ],
                "se" : [
                    "etik",
                    "lagstiftning",
                    "dataskydd",
                    "datasäkerhet",
                    "sekretess",
                    "ansvar",
                    "etisk",
                ],
                "en" : [
                    "ethics",
                    "law/legislation",
                    "confidentiality"
                    "privacy protection",
                    "responsibility",
                    "ethical",
                ]
            },
            "tutkimus- ja kehittämisosaaminen" : {
                "fi" : [
                    "tutkimus",
                    "innovaatio",
                    "kehittäminen"
                ],
                "se" : [
                    "forskning",
                    "innovation",
                    "utveckling",
                ],
                "en" : [
                    "research",
                    "innovation",
                    "development",
                ]
            },
            "robotiikka ja digitalisaatio" : {
                "fi" : [
                    "robotiikka",
                    "digi",
                    "tekoäly",
                    "sote-palvelut",
                    "tietoturva",
                    "tietosuoja",
                ],
                "se" : [
                    "robotik",
                    "digitalisering",
                    "digi",
                    "articifiell intelligens",
                    "service inom social- och hälsovård",
                    "sekretess",
                    "informationssäkerhet",
                ],
                "en" : [
                    "robotics",
                    "digi",
                    "artificial intelligence",
                    "social and health services",
                    "information security",
                    "information privacy",
                ]
            },
            "vaikuttavuus- kustannus- ja laatutietoisuus" : {
                "fi" : [
                    "laatu",
                    "laadun",
                    "vaikuttavuu",
                    "vaikutusten",
                    "kustannukset"
                ],
                "se" : [
                    "kvalitet",
                    "kvalit",
                    "effektivitet",
                    "effekt",
                    "kostnader",
                ],
                "en" : [
                    "quality",
                    "effective",
                    "effect",
                    "cost"
                ]
            },
            "kestävän kehityksen osaaminen" : {
                "fi" : [
                    "kestävä",
                    "ekolog",
                    "kestävyys",
                    "kierrätys",
                    "ympäristö",
                    "energiankulutus"
                ],
                "se" : [
                    "hållbar",
                    "ekolog",
                    "hållbarhet",
                    "sortera",
                    "miljö",
                    "omgivning",
                    "energiförbrukning",
                ],
                "en" : [
                    "sustainable",
                    "ecolog",
                    "sustainability",
                    "recycling",
                    "environment",
                    "energy consumption",
                ]
            },
            "viestintäosaaminen" : {
                "fi" : [
                    "viestintä",
                    "tunnetila",
                    "empatia",
                    "selkokieli",
                    "selko"
                ],
                "se" : [
                    "kommunikation",
                    "känslotillstånd",
                    "empati",
                    "klarspråk",
                    "klarhet",
                ],
                "en" : [
                    "communication",
                    "mood",
                    "emotional state",
                    "empathy",
                ]
            },
            "työntekijyysosaaminen" : {
                "fi" : [
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
                "se" : [
                    "kompetens",
                    "kunnande",
                    "kunskaper",
                    "färdigheter",
                    "ledarskap",
                    "arbetsvälmående",
                    "resiliens",
                    "karriärutveckling",
                    "nätverksarbete",
                    "arbetsgemenskap",
                    "interprofessionell",
                    "interprof",
                    "mångprofessionell",
                    "mångprof",
                ],
                "en" : [
                    "competence",
                    "know-how",
                    "lead",
                    "leading",
                    "management",
                    "managing",
                    "well-being at work",
                    "occupational health",
                    "industrial health",
                    "change skills",
                    "flexibility for change",
                    "change flexibility",
                    "career development",
                    "networking",
                    "working community",
                ]
            },
            "monialainen yhteistoiminta" : {
                "fi" : [
                    "monialaisuu",
                    "moniammatillisuu",
                    "monitiet",
                    "yhteistyö",
                    "verkostoituminen",
                    "asiantuntijuus"
                ],
                "se" : [
                    "mångsektoriell",
                    "mångvetenskaplig",
                    "mångdisciplinär",
                    "tvärsektoriell",
                    "sektorövergripande",
                    "yrkesövergripande",
                    "mångprofessionell",
                    "tvärvetenskaplig",
                    "samarbete",
                    "nätverksarbete",
                    "nätverksbildning",
                    "sakkunnig",
                    "expert",
                    "specialist",
                ],
                "en" : [
                    "multidisciplinary",
                    "multivocationality",
                    "multiprofessionalism",
                    "interprofessionalism",
                    "multidisciplinary",
                    "multi-disciplinary",
                    "cooperation",
                    "collaboration",
                    "co-operation",
                    "teamwork",
                    "liaison",
                    "networking",
                    "expertise",
                ]
            },
        }
        for facetFilter in ['et01.05.03', 'et01.04.03']:
            for osaaminen, hakusanat in hakusanat_dict.items():
                for hakusana in hakusanat.values():
                    for sana in hakusana:
                        for i in haeDataa(sana, facetFilter):
                            reg = re.match("(\d+).*", i.get('credits'))
                            if reg:
                                kurssi_obj = kurssi.Kurssi(
                                    re.sub(r'Avoin yo[:,\s]+', '', i.get('name')),
                                    reg.group(1),
                                    i.get('lopNames')[0],
                                    i.get('id'),
                                    "",
                                    osaaminen,
                                    "",
                                    ""
                                )
                            if i.get('id') not in objs:
                                objs[i.get('id')] = kurssi_obj
                            else:
                                if osaaminen not in objs[i.get('id')].osaamiset:
                                    objs[i.get('id')].osaamiset += "|"+osaaminen
        haeLisatiedot()
        tmp = objs
    except Exception as e:
        print(e)
        objs = tmp
def haeLisatiedot():
    for i, j in objs.items():
        data = haeKurssinTiedot(i)
        j.kieli = data.get('teachingLanguages')[0].lower()
        if data.get('teachingLanguages')[0].lower() in ['svenska']:
            j.kieli = "ruotsi"
        elif data.get('teachingLanguages')[0].lower() in ['english']:
            j.kieli = "englanti"
        
        j.postinumero = data.get('provider').get('postalAddress').get('postalCode')

        opetustyyppi_tmp = data.get("teachingPlaces") + data.get("formOfTeaching")
        for i in opetustyyppi_tmp:
            if i in ["Etäopetus", "Verkko-opetus", "Verkko-opiskelu",]:
                j.opetustyyppi = "etaopetus"
                continue
            elif i in ["Lähiopetus"]:
                j.opetustyyppi = "lahiopetus"
                continue
if __name__ == "__main__":
    pass
    # print("ok")
    # fo = open("test.json", "w")
    # fo.write(json.dumps(data, sort_keys=True, indent=2))
    # fo.close()
    #hakuTyokaluYksinkertainen()