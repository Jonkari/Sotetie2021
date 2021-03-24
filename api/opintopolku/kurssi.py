class Kurssi:
    def __init__(self, nimi, opintopisteet,  koulu,  id, kieli, osaamiset, opetustyyppi):
        """[summary]

        Args:
            nimi (string): Kurssin nimi
            opintopisteet (int): Kurssin opintopistemäärä
            koulu (string): Oppilaitos, missä kurssi on.
            id (string): Kurssin tunnus opintopolussa.
            kieli (string): Kurssin kieli.
            osaamiset (string): Kurssin osaamiset, erotettuna `|` merkillä.
            opetustyyppi (string): 
        """
        self.nimi = nimi
        self.opintopisteet = opintopisteet
        self.koulu = koulu
        self.id = id
        self.kieli = kieli
        self.osaamiset = osaamiset
        self.opetustyyppi = opetustyyppi
    def opintopolku_linkki(self,):
        """Ei tällä hetkellä käytössä oleva metodi, mutta näkee periaatteen miten opintopolun linkkitoimii

        Returns:
            string: Opintopolku.fi kurssi osoite
        """
        return "https://opintopolku.fi/app/#!/koulutus/{id}".format(
            id=self.id
        )
    def __str__(self):
        """toString metodi, mahdollisia konsol

        Returns:
            [type]: [description]
        """
        return str(self.nimi) + ", " + str(self.opintopisteet)
    def sqlYksinkertainen(self,):
        """Kurssin SQL lause

        Returns:
            string: SQL Lause tietokantaan
        """
        return "INSERT INTO kurssit (id, nimi, opintopisteet, koulu, osaamiset, kieli, opetustyyppi) VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\") ON DUPLICATE KEY UPDATE osaamiset=\"{}\";".format(
            self.id,
            self.nimi,
            self.opintopisteet,
            self.koulu,
            self.osaamiset,
            self.kieli,
            self.opetustyyppi,
            self.osaamiset
        )



