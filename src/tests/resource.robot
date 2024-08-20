*** Settings ***
Library  SeleniumLibrary  run_on_failure=NOTHING
# Library  ../../routes.py

*** Variables ***
${SERVER}       localhost:5000/
${BROWSER}      Chrome
${DELAY}        0.2 seconds
${HOME_URL}     http://${SERVER}
${LOGIN_URL}    http://${SERVER}/login

*** Keywords ***
Open Browser To Front Page
    Open Browser        ${HOME_URL}     ${BROWSER}
    Set Selenium Speed  ${DELAY}
    Front Page With Login Form Should Be Open

Open Browser To Login Page
    Open Browser        ${LOGIN_URL}    ${BROWSER}

Front Page With Login Form Should Be Open
    Title Should Be     Luetut kirjat

Input Username
    [Arguments]    ${username}
    Input Text    username    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    password    ${password}

Submit Credentials
    Click Button  Kirjaudu sisään

Main Page Should Be Open
    Location Should Be   ${HOME_URL}
    Title Should Be      Luetut kirjat
    Page Should Contain  Hei
    Page Should Contain  Etusivu
    Page Should Contain  Lukematta
    Page Should Contain  Lukeminen aloitettu
    Page Should Not Contain  Tunnus
    Page Should Not Contain  Salasana
