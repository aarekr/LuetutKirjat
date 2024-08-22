*** Settings ***
Resource  resource.robot

*** Test Cases ***
User Can Navigate To Add Book Page And It Displays Right Content
    Open Browser To Front Page
    Input Username    Olli
    Input Password    OllinSalasana12
    Submit Credentials
    Click link  Lisää kirja
    Page Should Contain  Anna kirjan tiedot
    Page Should Contain  Nimeke
    Page Should Contain  Kirjailija
    Page Should Contain  Kieli
    Close Browser

User Can Add A New Book To The Reading List
    Open Browser To Front Page
    Input Username    Olli
    Input Password    OllinSalasana12
    Submit Credentials
    Click link  Lisää kirja
    Input Book Title  Sinuhe
    Input Book Author  Mika Waltari
    Input Book Language  Suomi
    Submit Add New Book
    Page Should Contain  Kirjalistaan on nyt lisätty
    Page Should Contain  Sinuhe, Mika Waltari
    Click Link  Palaa etusivulle
    Page Should Contain  Sinuhe, Mika Waltari

User Can Mark Book As Reading Started
    Click Button  Aloita

User Can Mark Book As Reading Completed
    Click Button  Luettu
    Page Should Contain  Sinuhe, Mika Waltari
    Page Should Contain  ei arvosteltu

New Book Is Visible on Statistics Page
    Click link  Lukutilastot
    Page Should Contain  Tilastot
    Page Should Contain  Minun luetut kirjat
    Page Should Contain  Sinuhe
    Page Should Contain  Mika Waltari
    Page Should Contain  0
    Page Should Contain  Kaikki kirjat
    Page Should Contain  Lukijat
    Page Should Contain  1 kpl: Olli

User Can Press Book Info Button And Info Is Displayed
    Click link  Palaa etusivulle
    Click Button  Info
    Page Should Contain  Kirjan tiedot
    Page Should Contain  Nimeke
    Page Should Contain  Sinuhe
    Page Should Contain  Mika Waltari
    Page Should Contain  Luettu
    Page Should Contain  Kyllä
    Page Should Contain  Kieli
    Page Should Contain  Arvostelu puuttuu

User Can Rate A Book
    Page Should Contain  Arvostele kirja
    Select Radio Button  stars  4
    Click Button  Lisää arvostelu
    Page Should Contain  Sinuhe, Mika Waltari
    Page Should Contain  4 tähteä

Rated Book Shows As Rated On Statistics Page
    Click link  Lukutilastot
    Page Should Contain  Tilastot
    Page Should Contain  Minun luetut kirjat
    Page Should Contain  Sinuhe
    Page Should Contain  Mika Waltari
    Page Should Contain  4

User Can Add Another Book
    Click link  Palaa etusivulle
    Click link  Lisää kirja
    Input Book Title  Clean Code
    Input Book Author  Robert C. Martin
    Input Book Language  Englanti
    Submit Add New Book
    Page Should Contain  Kirjalistaan on nyt lisätty
    Page Should Contain  Clean Code, Robert C. Martin
    Click link  Palaa etusivulle
    Page Should Contain  Clean Code
    Page Should Contain  Robert C. Martin

Added Books Are Visible After User Logout And Login
    Click link  Kirjaudu ulos
    Input Username    Olli
    Input Password    OllinSalasana12
    Submit Credentials
    Page Should Contain  Sinuhe
    Page Should Contain  Mika Waltari
    Page Should Contain  Clean Code
    Page Should Contain  Robert C. Martin
    Page Should Contain  Clean Code
    Click Button  Aloita
    Click Button  Luettu
    Page Should Contain  ei arvosteltu
    Click link  Lukutilastot
    Page Should Contain  Tilastot
    Page Should Contain  Minun luetut kirjat
    Page Should Contain  Sinuhe
    Page Should Contain  Mika Waltari
    Page Should Contain  4
    Page Should Contain  Clean Code
    Page Should Contain  Robert C. Martin
    Page Should Contain  0

User Can Delete A Book
    Click link  Palaa etusivulle
    Click Button  Info
    Page Should Contain  Kirjan tiedot
    Click Button  Poista kirja
    Page Should Not Contain  Sinuhe
    Page Should Not Contain  Mika Waltari
    Click Button  Info
    Click Button  Poista kirja
    Page Should Not Contain  Clean Code
    Page Should Not Contain  Robert C. Martin
    Close Browser
