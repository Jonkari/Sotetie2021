import api
import requests
from testitapaus import testi_tapaus
import time
import threading
lista = []
threadien_maara = 30
tmp = []
lopeta = False
for i in range(threadien_maara):
    tmp.append(False)
def testi(ind):
    global tmp
    global lista
    url = 'http://137.74.119.216:5000'
    try:
        data = requests.get(url+"/api")
        testi_tapaus(data.status_code == 200, True, True, 1, "Status 200")
        data = requests.get(url+"/api/rajapinnat")
        testi_tapaus(data.status_code == 200, True, True, 2, "Status 200")
        count = 3
        for i in range(1):
            for nimi, rajapinta in data.json().items():
                try:
                    haku = requests.get(url+rajapinta)
                    testi_tapaus(haku.status_code == 200, True, True, count, "{} - Status 200".format(nimi))
                    count += 1
                    testi_tapaus(type(haku.json()) == list, True, True, count, "{} - tyyppi".format(nimi))
                    count += 1
                    lista.append(haku.elapsed.microseconds)
                except AssertionError as e:
                    print(e)
    except AssertionError as e:
        print(e)
    finally:
        tmp[ind] = True
def avg(tmp):
    summa = 0
    for i in tmp:
        summa += i
    return summa/len(tmp)
def median(tmp):
    return tmp[len(tmp)//3]
for i in range(threadien_maara):
    th = threading.Thread(target=testi, args=(i,))
    th.setDaemon(True)
    th.start()
while not lopeta:
    kaikkiTrue = True
    for i in tmp:
        if not i:
            kaikkiTrue = False
            break
    if kaikkiTrue:
        lopeta = True
    time.sleep(0.5)
else:
    print(len(lista))
    lista.sort()
    print(avg(lista))
    print(median(lista))


