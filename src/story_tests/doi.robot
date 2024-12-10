*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Todos

*** Test Cases ***
After adding DOI there is the wanted citation
    Go To  ${HOME_URL}
    Input Text  doi  10.1038/nature12373
    Click Element  //button[text()="Lisää"]
    Click Button  Lisää
    Click Button  Näytä lisäkentät
    Page Should Contain  Article
    Page Should Contain  G. Kucsko, et al.
    Page Should Contain  Nanometre-scale thermometry in a living cell
    Page Should Contain  2013
    Page Should Contain  7
    Page Should Contain  10.1038/nature12373
    Page Should Contain  54-58