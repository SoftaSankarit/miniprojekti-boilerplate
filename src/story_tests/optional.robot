*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Todos

*** Test Cases ***
After adding optional info, there is
    Go To  ${HOME_URL}
    Click Element  //button[text()='Lisää uusi viite']
    Scroll Element Into View  //a[.//span[@class='fi' and text()='Kirja']]
    Wait Until Element Is Visible  //a[.//span[@class='fi' and text()='Kirja']]
    Click Link  //a[.//span[@class='fi' and text()='Kirja']]
    Input Text  author  Erkki Esimerkki
    Input Text  title  Otsikko
    Input Text  publisher  Julkaisija
    Input Text  year  2024
    Click Button  Näytä lisäkentät
    Input Text  volume  Vol.23
    Input Text  note  Tämä on Erkki Esimerkkisen kirja
    Click Button  Lisää
    Click Button  Näytä lisäkentät
    Page Should Contain  Viitetyyppi
    Page Should Contain  Tekijät
    Page Should Contain  Otsikko
    Page Should Contain  Julkaisuvuosi
    Page Should Contain  Book
    Page Should Contain  Erkki Esimerkki
    Page Should Contain  Otsikko
    Page Should Contain  2024
    Page Should Contain  Vol.23
    Page Should Contain  Tämä on Erkki Esimerkkisen kirja