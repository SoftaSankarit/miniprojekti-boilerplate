*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Todos

*** Test Cases ***
At the start there are no books
    Go To  ${HOME_URL}
    Title Should Be  Viitesovellus
    Page Should Contain  Ei kirjoja tietokannassa.

After adding a book, there is one
    Go To  ${HOME_URL}
    Click Element  //button[text()='Lisää uusi viite']
    Click Link  //a[text()='Kirja']
    Input Text  author  Erkki Esimerkki
    Input Text  title  Otsikko
    Input Text  publisher  Julkaisija
    Input Text  year  2024
    Click Button  Lisää
    Page Should Contain  Tekijät
    Page Should Contain  Teoksen nimi
    Page Should Contain  Kustantaja
    Page Should Contain  Julkaisuvuosi
    Page Should Contain  Erkki Esimerkki
    Page Should Contain  Otsikko
    Page Should Contain  Julkaisija
    Page Should Contain  2024

After deleting a book, there are none
    Go To  ${HOME_URL}
    Click Element  //button[text()='Lisää uusi viite']
    Click Link  //a[text()='Kirja']
    Input Text  author  Erkki Esimerkki
    Input Text  title  Otsikko
    Input Text  publisher  Julkaisija
    Input Text  year  2024
    Click Button  Lisää
    Click Link  Poista
    Handle Alert  ACCEPT    
    Page Should Contain  Ei kirjoja tietokannassa.

After editing book values change
    Go To  ${HOME_URL}
    Click Element  //button[text()='Lisää uusi viite']
    Click Link  //a[text()='Kirja']
    Input Text  author  Erkki Esimerkki
    Input Text  title  Otsikko
    Input Text  publisher  Julkaisija
    Input Text  year  2024
    Click Button  Lisää
    Click Link  Muokkaa
    Input Text  year  2019
    Click Button  Tallenna muutokset
    Page Should Contain  Tekijät
    Page Should Contain  Teoksen nimi
    Page Should Contain  Kustantaja
    Page Should Contain  Julkaisuvuosi
    Page Should Contain  Erkki Esimerkki
    Page Should Contain  Otsikko
    Page Should Contain  Julkaisija
    Page Should Contain  2019
