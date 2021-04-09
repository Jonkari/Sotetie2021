    /**/
    $(document).ready(function () {
        
        function testiTapaus(funktio, muuttuja, boolean, testinro) {
            if(boolean) {
                console.assert(funktio() == muuttuja, `testi ${testinro}: ${muuttuja} != true`)
            } else {
                console.assert(funktio() != muuttuja, `testi ${testinro}: ${muuttuja} == true`)
            }
        }
        testiTapaus(valittuKieli, "suomi", false, 1); /*tutlkitaan onko heti sivustolle tullessa suunniteltu kielivalinta*/
        testiTapaus(valittuOpetustapa, "kaikkiTavat", false, 4);
        
        $(".radiorivi").click(function () {
        testiTapaus(valittuKieli, "suomi", false, 1); /*antaako klikkaillessa oikean kielivalinnan*/
        testiTapaus(valittuKieli, "ruotsi", true, 2);
        testiTapaus(valittuKieli, "englanti", true, 3);

        testiTapaus(valittuOpetustapa, "kaikkiTavat", false, 4);
        testiTapaus(valittuOpetustapa, "lahiopetus", true, 5);
        testiTapaus(valittuOpetustapa, "etaopetus", true, 6);
        console.log("testausta");
        })
        
        setTimeout(virheTilanne, 4000)
    });
    /**/