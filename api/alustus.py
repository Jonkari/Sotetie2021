"""
Käyttää opintopolku moduulia ja tekee tietokannan, ei ole varmaankaan viimeinen versio, taikka se mikä päivittyy viikon välein, mutta toimiva.
"""
if __name__ == "__main__":
    import tietokanta
    from opintopolku import opintopolku
    import asetukset
    import os
    import time

    db = tietokanta.Database(asetukset.palvelin, asetukset.kayttaja, asetukset.salasana, asetukset.tietokanta, asetukset.portti)

    db.query(
        """
        CREATE TABLE IF NOT EXISTS `kurssit` (
            `id` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
            `nimi` VARCHAR(200) NOT NULL COLLATE 'latin1_swedish_ci',
            `kieli` VARCHAR(30) NOT NULL COLLATE 'latin1_swedish_ci',
            `kuvaus` VARCHAR(500) NOT NULL DEFAULT '' COLLATE 'latin1_swedish_ci',
            `opintopisteet` INT(11) UNSIGNED NOT NULL DEFAULT '0',
            `koulu` VARCHAR(100) NOT NULL DEFAULT '0' COLLATE 'latin1_swedish_ci',
            `osaamiset` VARCHAR(500) NOT NULL DEFAULT '0' COLLATE 'latin1_swedish_ci',
            `opetustyyppi` VARCHAR(150) NULL DEFAULT '' COLLATE 'latin1_swedish_ci',
            `postinumero` VARCHAR(75) NULL DEFAULT '' COLLATE 'latin1_swedish_ci',
            PRIMARY KEY (`id`) USING BTREE
        )
        COLLATE='latin1_swedish_ci'
        ENGINE=InnoDB
        ;
        """
    )
    db.query("""
            CREATE TABLE IF NOT EXISTS `asetukset` (
            `tyyppi` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
            `data` INT(10) UNSIGNED NULL DEFAULT NULL,
            PRIMARY KEY (`tyyppi`) USING BTREE
            )
        COLLATE='latin1_swedish_ci'
        ENGINE=InnoDB
            ;
        """
    )
    db.query("""
    CREATE TABLE `cache` (
	`key` VARCHAR(75) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`value` LONGTEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	PRIMARY KEY (`key`) USING BTREE
    )
    COLLATE='utf8mb4_general_ci'
    ENGINE=InnoDB
    ;
    """)
    db.query("""
    CREATE TABLE IF NOT EXISTS `maakunnat` (
    `kunta` varchar(50) NOT NULL,
    `maakunta` varchar(50) NOT NULL,
    PRIMARY KEY (`kunta`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    """)
    db.query("""
    CREATE TABLE `postinumerot` (
	`postinumero` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'latin1_swedish_ci',
	`postitoimipaikka` VARCHAR(200) NOT NULL DEFAULT '' COLLATE 'latin1_swedish_ci',
	PRIMARY KEY (`postinumero`) USING BTREE
    )
    COLLATE='latin1_swedish_ci'
    ENGINE=InnoDB
    ;
    """)
    db.query(" ".join(open("api/maakunnat.sql", "r", encoding="utf-8").readlines()))
    db.query(" ".join(open("api/postinumerot.sql", "r", encoding="utf-8").readlines()))
    db.query("TRUNCATE asetukset")
    db.query("INSERT INTO asetukset (`tyyppi`, `data`) VALUES ('paivitetty.timestamp', 0)")
    db.query("INSERT INTO asetukset (`tyyppi`, `data`) VALUES ('paivitetty.kaynnissa', 1)")
    db.query("TRUNCATE kurssit")
    opintopolku.hakuTyokaluYksinkertainen()
    for i, j in opintopolku.objs.items():
        db.query(j.sqlYksinkertainen())
    db.query("UPDATE asetukset SET data={} WHERE tyyppi='paivitetty.kaynnissa'".format(0))
    db.query("UPDATE asetukset SET data={} WHERE tyyppi='paivitetty.timestamp'".format(time.time()))
    path = os.path.dirname(os.path.abspath(__file__))
    fo_api_ini = open(path+"/api.ini", "w")
    fo_api_ini.write("""
  [uwsgi]\n
  module = wsgi:app\n
  master = true\n
  processes = 2\n
  virtualenv = {path}\n
  socket = api.sock\n
  chmod-socket = 666\n
  vacuum = true\n
  \n
  die-on-term = true
      """.format(path=path))
    fo_api_ini.close()
    fo_wsgi_py = open(path+"/wsgi.py", "w")
    fo_wsgi_py.write("""from api import app\n
  \n
  if __name__ == "__main__":\n
      app.run()""")
    fo_wsgi_py.close()