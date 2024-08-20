*** Settings ***
Resource  resource.robot

*** Test Cases ***
User Can Log In With Right Username And Password
    Open Browser To Front Page
    Input Username    Olli
    Input Password    OllinSalasana12
    Submit Credentials
    Main Page Should Be Open
    Close Browser

User Cannot Log In With Wrong Password
    Open Browser To Front Page
    Input Username    Olli
    Input Password    WrongPass
    Submit Credentials
    Page Should Contain  Väärä tunnus tai salasana
    Page Should Not Contain  Lukematta
    Page Should Not Contain  Lukeminen aloitettu
    Page Should Not Contain  Hei, Olli
    Close Browser

User Cannot Log In With Wrong Username
    Open Browser To Front Page
    Input Username    Pekka
    Input Password    OllinSalasana12
    Submit Credentials
    Page Should Contain  Väärä tunnus tai salasana
    Page Should Not Contain  Lukematta
    Page Should Not Contain  Lukeminen aloitettu
    Page Should Not Contain  Hei, Olli
    Close Browser

User Cannot Log In Without Username And Password
    Open Browser To Front Page
    Submit Credentials
    Page Should Contain  Väärä tunnus tai salasana
    Page Should Not Contain  Lukematta
    Page Should Not Contain  Lukeminen aloitettu
    Page Should Not Contain  Hei, Olli
    Close Browser

User Can Log Out After Successful Login
    Open Browser To Front Page
    Input Username    Olli
    Input Password    OllinSalasana12
    Submit Credentials
    Main Page Should Be Open
    Click link  Kirjaudu ulos
    Page Should Not Contain  Lukematta
    Page Should Not Contain  Lukeminen aloitettu
    Page Should Not Contain  Hei, Olli
    Page Should Contain  Tunnus
    Page Should Contain  Salasana
    Close Browser

Login Page Can Be Opened And User Can Log In
    Open Browser To Login Page
    Input Username    Olli
    Input Password    OllinSalasana12
    Submit Credentials
    Main Page Should Be Open
    Click link  Kirjaudu ulos
    Page Should Not Contain  Lukematta
    Page Should Not Contain  Lukeminen aloitettu
    Page Should Not Contain  Hei, Olli
    Page Should Contain  Tunnus
    Page Should Contain  Salasana
    Close Browser