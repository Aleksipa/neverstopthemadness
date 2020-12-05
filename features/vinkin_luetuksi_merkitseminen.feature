# language: fi

Ominaisuus: Käyttäjä pystyy merkitsemään vinkin luetuksi tai lukemattomaksi

    Tapaus: Käyttäjä pystyy merkitsemään vinkin luetuksi
        Oletetaan että ollaan lähtötilanteessa
        Kun       käyttäjä vaihtaa vinkin luettu statusta
        Niin      käyttäjä näkee vinkkilistan, jossa vinkki on merkitty luetuksi
    Tapaus: Käyttäjä pystyy merkitsemään luetun vinkin lukemattomaksi
        Oletetaan että ollaan lähtötilanteessa
        Kun       käyttäjä vaihtaa vinkin luettu statusta
        Ja        käyttäjä vaihtaa vinkin luettu statusta
        Niin      käyttäjä näkee vinkkilistan, jossa vinkki on merkitty lukemattomaksi