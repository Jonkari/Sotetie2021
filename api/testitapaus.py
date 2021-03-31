


def testi_tapaus(testattava, muuttuja, totuusarvo, nro, lisatieto=""):
    if totuusarvo:
        assert testattava == muuttuja, "testi nro{} {}!={}, {}".format(nro, muuttuja, totuusarvo, lisatieto)
    else:
        assert testattava != muuttuja, "testi nro{} {}=={}, {}".format(nro, muuttuja, totuusarvo, lisatieto)