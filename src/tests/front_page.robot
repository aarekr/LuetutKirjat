*** Settings ***
Resource  resource.robot

*** Test Cases ***
Front Page Should Open With Right Content
    Open Browser To Front Page
    Title Should Be  Luetut kirjat
    Page Should Contain  Tunnus
    Page Should Contain  Salasana
    Page should Contain  Jos sinulla ei ole tunnusta
    Page Should Not Contain  Hei
    Close Browser

New Account Registration Link Is Visible And Can Be Clicked
    Open Browser To Front Page
    Click link  täällä
    Page Should Contain  Uuden käyttäjätilin rekisteröinti
    Page Should Contain  Käyttäjätunnus
    Page Should Contain  Salasana
    Click link  Palaa etusivulle
    Page Should Contain  Tunnus
    Page should Contain  Jos sinulla ei ole tunnusta
    Close Browser
