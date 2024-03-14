#!/bin/bash
# полный путь до скрипта
ABSOLUTE_FILENAME=`readlink -e "$0"`
# каталог в котором лежит скрипт
DIRECTORY=`dirname "$ABSOLUTE_FILENAME"`

echo "Скрипт запустился из папки $DIRECTORY"

if ! [ -f /opt/miac/inventory.txt ]; then /opt/miac/form-linux ; fi
