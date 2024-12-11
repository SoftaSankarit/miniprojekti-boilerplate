*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Todos

*** Test Cases ***
After search it only shows references that have the searchword in them
    Go To  ${HOME_URL}
    Click Element  //button[text()='Lisää uusi viite']
    Scroll Element Into View  //a[.//span[@class='fi' and text()='Kirja']]
    Wait Until Element Is Visible  //a[.//span[@class='fi' and text()='Kirja']]
    Click Link  //a[.//span[@class='fi' and text()='Kirja']]
    Input Text  author  Erkki Esimerkki
    Input Text  title  Otsikko
    Input Text  publisher  Julkaisija
    Input Text  year  2024
    Click Button  Lisää
    Click Element  //button[text()='Lisää uusi viite']
    Scroll Element Into View  //a[.//span[@class='fi' and text()='Kirja']]
    Wait Until Element Is Visible  //a[.//span[@class='fi' and text()='Kirja']]
    Click Link  //a[.//span[@class='fi' and text()='Kirja']]
    Input Text  author  Maija Meikäläinen
    Input Text  title  Haku testauksen alkeet 
    Input Text  publisher  OmatTaskut
    Input Text  year  2019
    Click Button  Lisää
    Input Text  query  Maija
    Click Button  Hae
    Page Should Contain  Viitetyyppi
    Page Should Contain  Tekijät
    Page Should Contain  Otsikko
    Page Should Contain  Julkaisuvuosi
    Page Should Contain  Book
    Page Should Contain  Maija Meikäläinen
    Page Should Contain  Haku testauksen alkeet
    Page Should Contain  2019