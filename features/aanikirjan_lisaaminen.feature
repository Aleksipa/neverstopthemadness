# language: fi

Ominaisuus: Käyttäjä pystyy lisäämään äänikirjan

    Tapaus: Käyttäjä menee lisäämään äänikirjaa
        Kun       käyttäjä avaa sivun äänikirjan lisäämiselle
        Niin      käyttäjä näkee oikeanlaisen äänikirjan formin
    Tapaus: Käyttäjä lisää validin äänikirjan
        Kun        käyttäjä täyttää äänikirjan lomakkeen oikein
         Ja        käyttäjä lähettää lomakkeen
         Niin      äänikirja lisätään vinkkeihin
    Tapaus: Käyttäjä lisää epävalidin äänikirjan
        Kun        käyttäjä täyttää äänikirjan lomakkeen väärin
         Ja        käyttäjä lähettää lomakkeen
         Niin      äänikirjaa ei lisätä vinkkeihin