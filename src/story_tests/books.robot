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
    Click Link  Lisää uusi kirja
    Input Text  author  Erkki Esimerkki
    Input Text  title  Otsikko
    Input Text  publisher  Julkaisija
    Input Text  year  2024
    Click Button  Submit
    Page Should Contain  Author
    Page Should Contain  Title
    Page Should Contain  Publisher
    Page Should Contain  Year
    Page Should Contain  Erkki Esimerkki
    Page Should Contain  Otsikko
    Page Should Contain  Julkaisija
    Page Should Contain  2024

After deleting a book, there are none
    Go To  ${HOME_URL}
    Click Link  Lisää uusi kirja
    Input Text  author  Erkki Esimerkki
    Input Text  title  Otsikko
    Input Text  publisher  Julkaisija
    Input Text  year  2024
    Click Button  Submit
    Click Link  Poista
    Page Should Contain  Ei kirjoja tietokannassa.