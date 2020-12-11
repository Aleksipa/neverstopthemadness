# language: fi

Ominaisuus: Käyttäjä pystyy muokkaamaan elokuvaa

    Tapaus: Käyttäjä menee muokkamaan elokuvaa
        Oletetaan että ollaan lähtötilanteessa
        Kun       käyttäjä avaa sivun elokuvan muokkaamiselle
        Niin      käyttäjä näkee oikeanlaisen elokuvan muokkaus formin

    Tapaus: Käyttäjä lisää validin muutoksen elokuvaan
        Oletetaan että ollaan lähtötilanteessa
        Kun       käyttäjä täyttää elokuvan muokkauslomakkeen oikein
        Ja        käyttäjä lähettää lomakkeen
        Niin      muokattu elokuva löytyy vinkeistä

    Tapaus: Käyttäjä lisää epävalidin muutoksen elokuvaan
        Oletetaan että ollaan lähtötilanteessa
        Kun       käyttäjä täyttää elokuvan muokkauslomakkeen väärin
        Ja        käyttäjä lähettää lomakkeen
        Niin      elokuva ei muokkaannu