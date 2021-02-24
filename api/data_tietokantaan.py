if __name__ == "__main__":
    import tietokanta
    from opintopolku import opintopolku

    db = tietokanta.Database("localhost", "root", "", "wordpress")

    db.query(
        """
            CREATE TABLE IF NOT EXISTS `kurssit` (
            `id` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
            `nimi` VARCHAR(100) NOT NULL COLLATE 'latin1_swedish_ci',
            `kieli` VARCHAR(30) NOT NULL COLLATE 'latin1_swedish_ci',
            `kuvaus` VARCHAR(500) NOT NULL COLLATE 'latin1_swedish_ci',
            `opintopisteet` INT(11) UNSIGNED NOT NULL DEFAULT '0',
            `koulu` VARCHAR(50) NOT NULL DEFAULT '0' COLLATE 'latin1_swedish_ci',
            `osaamiset` VARCHAR(150) NOT NULL DEFAULT '0' COLLATE 'latin1_swedish_ci',
            PRIMARY KEY (`id`) USING BTREE
        )
        COLLATE='latin1_swedish_ci'
        ENGINE=InnoDB
        ;
        """
    )
    db.query("TRUNCATE kurssit")
    opintopolku.hakuTyokaluYksinkertainen()
    for i, j in opintopolku.objs.items():
        db.query(j.sqlYksinkertainen())
