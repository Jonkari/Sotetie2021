class Kurssi:
    def __init__(self, nimi, opintopisteet, kuvaus, koulu, paikka, id, tyyppi, kieli, aloitus_timestamp, loppu_timestamp):
        self.nimi = nimi
        self.opintopisteet = opintopisteet
        self.kuvaus = kuvaus
        self.koulu = koulu
        self.paikka = paikka
        self.id = id
        self.tyyppi = tyyppi
        self.kieli = kieli
        self.aloitus_timestamp = aloitus_timestamp
        self.loppu_timestamp = loppu_timestamp
    def opintopolku_linkki(self,):
        return "https://opintopolku.fi/app/#!/koulutus/{id}".format(
            id=self.id
        )
    def __str__(self):
        return self.nimi + ", " + self.opintopisteet + ", " + self.kuvaus
    def testaa(self,):
        if not self.nimi or not self.opintopisteet or not self.kuvaus or not self.koulu or not self.paikka or not self.id or not self.tyyppi or not self.kieli or not self.aloitus_timestamp or not self.loppu_timestamp:
            print(self.id)
            print(self.nimi)
            print(self.paikka)
            print(self.tyyppi)
            print(self.kieli)
            print(self.aloitus_timestamp)
            print(self.loppu_timestamp)
            return True
        return False



