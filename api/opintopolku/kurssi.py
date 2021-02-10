class Kurssi:
    def __init__(self, nimi, opintopisteet,  koulu,  id, kieli, osaamiset):
        self.nimi = nimi
        self.opintopisteet = opintopisteet
        self.koulu = koulu
        self.id = id
        self.kieli = kieli
        self.osaamiset = osaamiset
    def opintopolku_linkki(self,):
        return "https://opintopolku.fi/app/#!/koulutus/{id}".format(
            id=self.id
        )
    def __str__(self):
        return str(self.nimi) + ", " + str(self.opintopisteet)
    def sqlYksinkertainen(self,):
        return "INSERT INTO kurssit (id, nimi, opintopisteet, koulu, osaamiset) VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\") ON DUPLICATE KEY UPDATE osaamiset=\"{}\";".format(
            self.id,
            self.nimi,
            self.opintopisteet,
            self.koulu,
            self.osaamiset,
            self.osaamiset
        )



