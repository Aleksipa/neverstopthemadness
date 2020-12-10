# language: fi

Ominaisuus: Käyttäjä pystyy muokkaamaan videota

    Tapaus: Käyttäjä menee muokkamaan videota
        Oletetaan että ollaan lähtötilanteessa
        Kun       käyttäjä avaa sivun videon muokkaamiselle
        Niin      käyttäjä näkee oikeanlaisen video formin

    Tapaus: Käyttäjä lisää validin muutoksen videoon
        Oletetaan että ollaan lähtötilanteessa
        Kun       käyttäjä täyttää videon muokkauslomakkeen oikein
        Ja        käyttäjä lähettää lomakkeen
        Niin      muokattu video löytyy vinkeistä

    Tapaus: Käyttäjä lisää epävalidin muutoksen kirjaan
        Oletetaan että ollaan lähtötilanteessa
        Kun       käyttäjä täyttää video lomakkeen väärin
        Ja        käyttäjä lähettää lomakkeen
        Niin      video ei muokkaannu