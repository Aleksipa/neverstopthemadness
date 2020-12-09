# language: fi

Ominaisuus: Käyttäjä pystyy lisäämään elokuvan

    Tapaus: Käyttäjä menee lisäämään elokuvaa
        Kun       käyttäjä avaa sivun elokuvan lisäämiselle
        Niin      käyttäjä näkee oikeanlaisen elokuvan formin
    Tapaus: Käyttäjä lisää validin elokuvan
        Kun        käyttäjä täyttää elokuvan lomakkeen oikein
         Ja        käyttäjä lähettää lomakkeen
         Niin      elokuva lisätään vinkkeihin
    Tapaus: Käyttäjä lisää epävalidin elokuvan
        Kun        käyttäjä täyttää elokuvan lomakkeen väärin
         Ja        käyttäjä lähettää lomakkeen
         Niin      elokuvaa ei lisätä vinkkeihin