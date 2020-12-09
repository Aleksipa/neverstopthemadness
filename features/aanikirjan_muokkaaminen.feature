# language: fi

Ominaisuus: Käyttäjä pystyy muokkaamaan äänikirjaa

    Tapaus: Käyttäjä menee muokkamaan äänikirjaa
        Oletetaan että ollaan lähtötilanteessa
        Kun       käyttäjä avaa sivun äänikirjan muokkaamiselle
        Niin      käyttäjä näkee oikeanlaisen äänikirjan formin
    Tapaus: Käyttäjä lisää validin muutoksen äänikirjaan
        Oletetaan että ollaan lähtötilanteessa
        Kun       käyttäjä täyttää äänikirjan muokkauslomakkeen oikein
         Ja        käyttäjä lähettää lomakkeen
         Niin      muokattu äänikirja löytyy vinkeistä
    Tapaus: Käyttäjä lisää epävalidin muutoksen äänikirjaan
        Oletetaan että ollaan lähtötilanteessa
        Kun       käyttäjä täyttää äänikirjan muokkauslomakkeen väärin
         Ja        käyttäjä lähettää lomakkeen
         Niin      muokattua äänikirjaa ei löydy vinkeistä