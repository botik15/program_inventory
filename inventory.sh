##!/bin/bash
#
#if [ "$EUID" -ne 0 ]
#  then echo "Пожалуйста, запустите как root!"
#  exit
#fi
#
## полный путь до скрипта
#ABSOLUTE_FILENAME=`readlink -e "$0"`
## каталог в котором лежит скрипт
#DIRECTORY=`dirname "$ABSOLUTE_FILENAME"`
#
#echo "Скрипт запустился из папки $DIRECTORY"
#
#echo -e "\e[1;31m
#>Будут скачены все необходимые файлы для Инвентаризация>!<
#
#Об ошибках в скрипте пишите в МИАЦ, не забывая прикладывать Логи и конфиги (иначе помощь будет \"пальцем в небо\")
#\e[0m"
#echo "Скачать файлы? (Y(y)/N(n))"
#read item
#case "$item" in
#y|Y) echo -e "\e[1;32mВы ввели «y|Y»\e[0m"
#
#    ;;
#n|N) echo -e "\e[1;33mВы ввели «n|N»\e[0m"
#exit 0
#        ;;
#*) echo -e "\e[1;33mНичего не ввели. Выполняем действие по умолчанию (Без настроек)\e[0m"
#exit 0
#        ;;
#esac
#
#
#
##                             //Дополнительно
##
##---------------------------------------------------------------------------------------------
##удаление файлов
#rm /opt/miac/inventory/log.txt
#rm /opt/miac/inventory/inventory.text
#rm /opt/miac/inventory/inventory.json
#rm /opt/miac/inventory/info.json
#rm /opt/miac/script/inventDataPC-miac.sh
#rm /opt/miac/script/inventProgramm-miac.sh
#rm /opt/miac/form-linux
#rm /opt/miac/main-linux
#rm /opt/miac/connect-linux
#rm /opt/miac/dist.tar.gz
#
##-------Инвентаризация форма
##создает папку /opt/miac
#mkdir -p /opt/miac
#chmod -R 777 /opt/miac
#
##создает папку /opt/miac/inventory
#mkdir -p /opt/miac/inventory
#chmod -R 777 /opt/miac/inventory
#
##создает папку /opt/miac/script/
#mkdir -p /opt/miac/script/
#chmod -R 777 /opt/miac/script/
#
##библиотеки для подключения к бд
#sudo apt-get install libpq-dev
#sudo apt-get install libjsoncpp-dev
#sudo ln -s /usr/include/jsoncpp/json/ /usr/include/json
#
##нужно скачать файлы dist.tar.gz и добавить права
#wget -P /opt/miac/ --no-proxy http://smio.med.cap.ru/media/dist.tar.gz
#chmod +x /opt/miac/dist.tar.gz
#
#tar -xzvf /opt/miac/dist.tar.gz -C /opt/miac/
#
#
#
## #создает ярлык автозапуска
## cat /dev/null > /etc/xdg/autostart/inventDataPC-miac.desktop
##     echo "
##     [Desktop Entry]
##     Name[ru]=inventDataPC-miac.desktop
##     Type=Application
##     NoDisplay=false
##     Exec=/opt/miac/script/inventDataPC-miac.sh
##     Hidden=false
##     Terminal=false
##     StartupNotify=false"> /etc/xdg/autostart/inventDataPC-miac.desktop
#
#
#
##-------Инвентаризация программа
#
#
#
##cat /dev/null > /etc/xdg/autostart/inventProgramm-miac.desktop
##    echo "
##    [Desktop Entry]
##    Name[ru]=inventProgramm-miac.desktop
##    Type=Application
##    NoDisplay=false
##    Exec=/opt/miac/script/inventProgramm-miac.sh
##    Hidden=false
##    Terminal=false
##    StartupNotify=false"> /etc/xdg/autostart/inventProgramm-miac.desktop
##
#
chmod -R 777 /opt/miac
#
#
#/opt/miac/main-linux
