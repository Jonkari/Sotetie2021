

import traceback
def testi_tapaus(testattava, muuttuja, totuusarvo, nro, lisatieto=""):
    if totuusarvo:
        assert testattava == muuttuja, "Testi nro{} {}!={}, {}".format(nro, muuttuja, totuusarvo, lisatieto)
    else:
        assert testattava != muuttuja, "Testi nro{} {}=={}, {}".format(nro, muuttuja, totuusarvo, lisatieto)
try:
    testi_tapaus(0 == 0, True, True, 1)
    testi_tapaus(0 == 0, True, True, 2)
except AssertionError as e:
    traceback.print_exc()
    print(e)    