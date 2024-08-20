*** Settings ***
Library  SeleniumLibrary  run_on_failure=NOTHING
Library  ../../routes.py

*** Variables ***
${SERVER}       localhost:5000
${BROWSER}      Firefox
${DELAY}        0 seconds
${HOME_URL}     http://${SERVER}

*** Keywords ***
Open Browser To Front Page
    Open Browser        ${HOME_URL}    ${BROWSER}
    Set Selenium Speed  ${DELAY}
    Front Page With Login Form Should Be Open

Front Page With Login Form Should Be Open
    Title Should Be     Luetut kirjat


#Go To Home Page
#    Go To  ${HOME_URL}

#Linktest
#    Click link  Lukutilastot
