# CUPS Web Interface (RU)
![Интерфейс](https://redabyq.space/images/github/cupswebinterface.png")
##  1. Установка и запуск
<span style="color: Yellow">- </span>Сначала <span style="color: cyan">клонируем репозиторий:</span>

     git clone https://github.com/redabyq/cups_web_interface

<span style="color: Yellow">- </span>Перейдем в папку и запустим <span style="color: Green">скрипт</span>:

    sudo bash run.sh
    
<span style="color: Yellow">- </span>Если планируется использование в <b>локальной сети</b>, откроем порт:

    sudo ufw allow 8780
##  2. Зависимости
### <span style="color: orange"> Для правильной работы скрипта необходим LibreOffice, а так же установленный CUPS!
### LibreOffice

    sudo add-apt-repository ppa:libreoffice/ppa
    sudo apt update
    sudo apt install libreoffice
### CUPS
    sudo apt install cups
##
#
# CUPS Web Interface (ENG)
##  1. Installation and launch
<span style="color: Yellow">- </span>First, <span style="color: cyan">clone the repository:</span>

     git clone https://github.com/redabyq/cups_web_interface

<span style="color: Yellow">- </span></span>Go to the folder and run the <span style="color: Green">script:

    sudo bash run.sh
    
<span style="color: Yellow">- </span>If you plan to use it on a <b>local network</b>, open the port:

    sudo ufw allow 8780
##  2. Requirements
### <span style="color: orange"> For the script to work correctly, LibreOffice is required, as well as CUPS installed!
### LibreOffice

    sudo add-apt-repository ppa:libreoffice/ppa
    sudo apt update
    sudo apt install libreoffice

### CUPS
    sudo apt install cups