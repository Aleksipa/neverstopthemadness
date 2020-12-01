# language: fi

Ominaisuus: Käyttäjä pystyy lisäämään videon

    Tapaus: Käyttäjä menee lisäämään videota
        Kun       käyttäjä avaa sivun videon lisäämiselle
        Niin      käyttäjä näkee oikeanlaisen video formin
    Tapaus: Käyttäjä lisää validin videon
        Kun        käyttäjä täyttää video lomakkeen oikein
         Ja        käyttäjä lähettää lomakkeen
         Niin      video lisätään vinkkeihin
    Tapaus: Käyttäjä lisää epävalidin videon
        Kun        käyttäjä täyttää video lomakkeen väärin
         Ja        käyttäjä lähettää lomakkeen
         Niin      videota ei lisätä vinkkeihin