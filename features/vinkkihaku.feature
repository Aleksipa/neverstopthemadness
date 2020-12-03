# language: fi

Ominaisuus: Käyttäjä voi hakea vinkkejä yhdellä kriteerillä

    Tapaus: Käyttäjä listaa kaikki vinkit
        Oletetaan että ollaan lähtötilanteessa
        Kun       käyttäjä avaa vinkkisivun
        Niin      kaikki vinkit näkyvät
    
    Tapaus: Käyttäjä hakee vinkkejä yhdellä ehdolla
        Oletetaan että ollaan lähtötilanteessa
        Kun  käyttäjä avaa vinkkisivun
        Ja   hakee ehdon "isbn" arvolla "978-0132350884"
        Niin ainoastaan vinkki "Clean Code: A Handbook of Agile Software Craftsmanship" näkyy
