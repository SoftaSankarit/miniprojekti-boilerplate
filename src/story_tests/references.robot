*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Todos

*** Test Cases ***
After adding multiple types of references, they all show
    Go To  ${HOME_URL}
    Click Element  //button[text()='Lisää uusi viite']
    Wait Until Element Is Visible  //a[.//span[@class='fi' and text()='Kirja']]
    Scroll Element Into View  //a[.//span[@class='fi' and text()='Kirja']]
    Click Link  //a[.//span[@class='fi' and text()='Kirja']]
    Input Text  author  Erkki Esimerkki
    Input Text  title  Hyvä Kirjan Nimi
    Input Text  publisher  Kirjat Oy
    Input Text  year  2024
    Click Button  Lisää

    Click Element  //button[text()='Lisää uusi viite']
    Wait Until Element Is Visible  //a[.//span[@class='fi' and text()='Artikkeli']]
    Scroll Element Into View  //a[.//span[@class='fi' and text()='Artikkeli']]
    Click Link  //a[.//span[@class='fi' and text()='Artikkeli']]
    Input Text  author  Arti Artikkeli
    Input Text  title  Hyvä Artikkelin nimi
    Input Text  journal  Journalit Oy
    Input Text  year  2024
    Click Button  Lisää

    Click Element  //button[text()='Lisää uusi viite']
    Wait Until Element Is Visible  //a[.//span[@class='fi' and text()='Konferenssi']]
    Scroll Element Into View  //a[.//span[@class='fi' and text()='Konferenssi']]
    Click Link  //a[.//span[@class='fi' and text()='Konferenssi']]
    Input Text  author  Konfe Konferenssi
    Input Text  title  Hyvä Konferenssin nimi
    Input Text  booktitle  Konferenssit Kirja Nimi
    Input Text  year  2024
    Click Button  Lisää

    Click Element  //button[text()='Lisää uusi viite']
    Wait Until Element Is Visible  //a[.//span[@class='fi' and text()='Väitöskirja']]
    Scroll Element Into View  //a[.//span[@class='fi' and text()='Väitöskirja']]
    Click Link  //a[.//span[@class='fi' and text()='Väitöskirja']]
    Input Text  author  Väinö Väitöskirja
    Input Text  title  Väitöskirjan Ohjelmoinnista
    Input Text  school  Helsingin Yliopisto
    Input Text  year  2024
    Click Button  Lisää

    Page Should Contain  Book
    Page Should Contain  Conference
    Page Should Contain  Article
    Page Should Contain  Phdthesis
    