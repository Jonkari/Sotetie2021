
    var genOsaamiset = null;
    var koulut = null;
    var avattu = false;
    var valittu = true;
    var kieli = "suomi";
    var opetustapa = "kaikkiTavat";
    var maakuntaMap = new Map();
    //var osoite = "http://137.74.119.216:5000"; //"http://137.74.119.216:5000/"

    // näkyviin ilmoitus, jos tietokantaan ei saada yhteyttä 
    function virheTilanne() {
        document.getElementById("kurssiTaulu").style.display = "none";
        document.getElementById("eiYhteytta").style.display = "block";
    };

    //mikä kieli valittu
    function valittuKieli() {
        var vaihtoehdot = document.getElementsByName('kieli');
        for (i = 0; i < vaihtoehdot.length; i++) {
            if (vaihtoehdot[i].checked)
                return vaihtoehdot[i].value;
        }
    }

    //mikä opetustapa valittu
    function valittuOpetustapa() {
        var vaihtoehdot = document.getElementsByName('tapa');
        for (i = 0; i < vaihtoehdot.length; i++) {
            if (vaihtoehdot[i].checked)
                return vaihtoehdot[i].value;
        }
    }

    function paivitaMaara() {
        var checkboxes = jQuery('input.checkboxKoulut:checked').length;
        var koulut_nro = document.querySelector(".nakyvaMaara")
        var html = ``
        var option = `<option>${checkboxes} koulua valittu</option>`
        html += option
        koulut_nro.innerHTML = html
    }

    jQuery(document).ready(function () {

        document.addEventListener("click", function (e) {
            if (e.target && (e.target.matches(".kouluLista"))) {
                if (avattu) {
                    document.querySelector(".koulu").style.display = "none";
                    avattu = false;
                }
                else {
                    document.querySelector(".koulu").style.display = "block";
                    avattu = true;
                }
            }
            else {
                if (e.target && (e.target.matches(".checkboxKoulut") || e.target.matches('.koulu *'))) {
                } else {
                    document.querySelector(".koulu").style.display = "none";
                    avattu = false;
                }
            }
        });

        //maakuntavalikon klikkaus
        jQuery(".maakunnat").on("click", function () {
            var koulut = document.querySelectorAll(".checkboxKoulut");

            if (this.value == "kaikki") {
                for (var x of koulut) {
                    x.checked = true;
                }
                document.querySelector("#kaikki").checked = true;
                valittu = true;
            }
            else {
                document.querySelector("#kaikki").checked = false;
                for (var x of koulut) {
                    if (maakuntaMap.get(this.value).includes(x.value)) {
                        x.checked = true;
                    }
                    else {
                        x.checked = false;
                    }
                }
                valittu = false;
            }
            paivitaMaara();
        })

        jQuery(".koulu").on("click", "#kaikki", function () {
            var x = document.querySelectorAll(".checkboxKoulut");
            for (var i of x) {
                if (valittu) {
                    i.checked = false;
                }
                else {
                    i.checked = true;
                }
            }

            if (valittu) {
                valittu = false;
            }
            else {
                valittu = true;
                document.querySelector(".maakunnat").value = "kaikki";
            }

        })

        //kuinka monta koulua valittu
        jQuery("#kouluValikko").click(function () {
            paivitaMaara();
        })

        //asetetaan muuttujiin kieli ja opetustapa
        jQuery(".painikkeet").click(function () {
            kieli = valittuKieli();
            opetustapa = valittuOpetustapa();
        })

        //haetaan aiheet valikkoon:
        jQuery.get(osoite + "/api/rajapinnat", function (data) {
            genOsaamiset = jQuery.extend({}, { "Kaikki": "/api/" }, data);
            var genOsaamiset_select = document.querySelector(".aihe")
            var html = ``
            for (var i in genOsaamiset) {
                var option = `<option value="${i}">${i}</option>`
                html += option
            }
            genOsaamiset_select.innerHTML = html
            try {
                if (valmisHaku !== undefined) {
                    valmisHaku(genOsaamiset)
                }
            } catch (error) { }
            fetch(genOsaamiset_select.options[genOsaamiset_select.selectedIndex].value);
        })
            .fail(virheTilanne);

        //haetaan koulut valikkoon:
        var maakuntaSet = new Set();
        jQuery.get(osoite + "/api/koulut", function (data) {
            koulut = data;
            var korkeaKoulu_select = document.querySelector(".koulu")
            var html = `<label><input type="checkbox" checked id="kaikki"/>Kaikki / Tyhjennä</label>`
            for (var i in koulut) {
                var option = `<label><input class="checkboxKoulut" type="checkbox" checked value="${koulut[i].koulu}"/>${koulut[i].koulu}</label>` /*`<option value="${koulut[i].koulu}">${koulut[i].koulu}</option>`*/
                html += option
            }
            korkeaKoulu_select.innerHTML = html;
            paivitaMaara();

            //haetaan maakunnat valikkoon:
            maakunnat = data
            var maakunnat_select = document.querySelector(".maakunnat")
            var html = `<option value="kaikki">Kaikki</option>` 
            for (var i in maakunnat) {
                maakuntaSet.add(maakunnat[i].maakunta);
            }
            maakuntaSet.forEach(function (value) {
                var option = `<option value="${value}">${value}</option>`
                html += option
            })
            maakunnat_select.innerHTML = html

            //maakunnat valikon toiminnallisuus:
            //maakuntaMap

            for (var i in maakunnat) {
                if (maakuntaMap.has(maakunnat[i].maakunta)) {
                    maakuntaMap.get(maakunnat[i].maakunta).push(maakunnat[i].koulu);
                }
                else {
                    maakuntaMap.set(maakunnat[i].maakunta, [maakunnat[i].koulu]);
                }
            }
        })
            .fail(virheTilanne)

        //Haetaan viimeisimmän päivityksen päivämäärä:
        jQuery.get(osoite + "/api/paivitys", function (data) {
            let onkokaynnissa = 0;
            let paivitystimestamp = 0;
            for (let asetus of data) {
                if (asetus.tyyppi == "paivitetty.kaynnissa") {
                    onkokaynnissa = asetus.data
                } else if (asetus.tyyppi == "paivitetty.timestamp") {
                    paivitystimestamp = asetus.data
                }
            }
            var paivitys = new Date(paivitystimestamp * 1000);
            var kuukausi = paivitys.getMonth() + 1;
            var paiva = paivitys.getDate();
            var vuosi = paivitys.getFullYear();
            var paivittymassa = onkokaynnissa == 1 ? "Tietokanta on päivittymässä" : "";
            document.getElementById("paivitys").innerHTML = `${paivittymassa}<br>Päivitetty: ${paiva}.${kuukausi}.${vuosi}`;
        }).fail(virheTilanne)

        //otetaan kiinni aihe mikä on valittu:
        jQuery('#haeNappi').click(() => {
            var geneerinenAlue = document.querySelector(".aihe");
            var aihe = geneerinenAlue.options[geneerinenAlue.selectedIndex].value; //antaa esim. "aihe5" eli Tutkimus.
            fetch(aihe);
        });

        fetch = (aihe) => {
            var osoiteUrl = osoite + genOsaamiset[aihe];
            jQuery.get({
                url: osoiteUrl,
                success: (result) => {
                    jQuery("#data tbody").html("");
                    showResultInTable(result);
                }
            }).fail(virheTilanne);
        }

    });

    //laitetaan haetut tiedot Löydetyt opintojaksot -tauluun:

    showResultInTable = (result) => {
        var valitut = new Set();
        var checkBoxes = document.querySelectorAll(".checkboxKoulut")

        for (var x of checkBoxes) {
            if (x.checked) {
                valitut.add(x.value)
            }
        }
        var nro = 0;
        html = ``

        result.forEach(element => {
            if (valitut.has(element.koulu) && element.kieli.includes(kieli) && (opetustapa == "kaikkiTavat" || element.opetustyyppi == opetustapa)) {
                let opintojaksot = ""
                opintojaksot += `<td colspan="2"><a target="_blank" href="https://opintopolku.fi/app/#!/koulutus/${element.id}">${element.nimi} (${element.opintopisteet} op)</a></td>\n`;
                opintojaksot += "<td colspan=\"2\">" + element.koulu + "</td>\n";
                opintojaksot += "</tr>\n";
                html += opintojaksot
                nro++;
            }
        });
        document.getElementById("tauluOtsikko").innerHTML = "Löydetyt opintojaksot (" + nro + " kpl)";
        document.getElementById("kurssiTaulu").style.display = "block";
        document.getElementById("eiKursseja").style.display = "none";
        document.getElementById("eiYhteytta").style.display = "none";


        if (html.length == 0) {
            document.getElementById("eiKursseja").style.display = "block";
            document.getElementById("kurssiTaulu").style.display = "none";
            document.getElementById("eiYhteytta").style.display = "none";
        }
        document.querySelector("#data tbody").innerHTML = html;
    }

