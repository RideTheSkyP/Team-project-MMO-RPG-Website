$stats
========

Aby uruchomić wyśwtelanie statystyk na stronie:
----------

    uruchomienie strony wg instrukcji (w tym `python3 manage.py migrate`) 
    uruchomienie skryptu baza_staty.sql w wybranej bazie MySQL
    standardowe uruchomienie za pomocą `python3 manage.py runsslserver []`

Obsługa API:
--------

API posiada własny link `[strona]/api/[zapytanie]`

Dostępne zapytania:
- `test` - zwraca czy API działa
- `top_players_all` - zwraca całą tabelę `top_players` z przetworzonymi danymi
- `top_maps` - zwraca statystyki map
- `player/[player]` - zwraca wszystskie gry danego gracza

### format danych

Installation
------------

Install $project by running:

    install project
