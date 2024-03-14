# -*- coding: utf-8 -*-
import json
import multiprocessing
import os

from chek_text import check_inventary_text
from form import application
from os_info import os_files
from other_file import check_inventar, log_append

#создание json файла
def create_json_invetnory():
    log_append("Создание json <<Инвентаризации>>")
    data = {}
    data['Form info'] = []
    data['Form info'].append({'Медицинская организация': '',
                              'Регион': '',
                              'Населенный пункт': '',
                              'Улица/Пр-кт/Площадь': '',
                              'Дом': '',
                              'Инвентраный номер': '',
                              'Серийный номер': '',
                              'Год ввода в эксплуатацию': '',
                              'Тип подключения': ''
                              })
    with open(str(check_inventar()[1]), 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    log_append("Запуск формы")



# чтение данных компа и запись в json
def create_json_info():
    os_file = os_files()
    data = {}
    data['Comp info'] = []
    data['Comp info'].append(
        {'ИМЯ': os_file[0], 'IP': os_file[1], 'MAC': os_file[2], 'ОС': os_file[3], 'РЕЛИЗ': os_file[4],
         'Антивирус': os_file[5], 'WINE': os_file[6],
         'SecretNET': os_file[7], 'ПРОЦЕССОР': os_file[8], 'ФИЗ. / ВСЕГО ЯДЕР / ОПЕРАТИ.. ПАМЯТЬ	': os_file[9],
         'ВСЕГО / СВОБО.. ДИСКА	': os_file[10], 'Таблица': 'main_model_hospital_' + os_file[0].split('-')[0]

         })
    log_append("Запись в json <<Информация о системе>>")
    with open(str(check_inventar()[3]), 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)


# проверка на наличие заполенение данных
def load_json_inventory():
    with open(str(check_inventar()[1])) as json_file:
        data = json.load(json_file)
        for p in data['Form info']:
            mass = [p['Медицинская организация'],
                 p['Регион'],
                 p['Населенный пункт'],
                 p['Улица/Пр-кт/Площадь'],
                 p['Дом'],
                 p['Структурное подразделение'],
                 p['Инвентраный номер'],
                 p['Серийный номер'],
                 p['Год ввода в эксплуатацию'],
                 p['Тип подключения']]

            for item in mass:
                if item == '':
                    application()  # Запск формы
                    log_append("Запуск формы, не заполнены все данные")

#запск c++ для отправки данных
def connect():

    # subprocess.run('/opt/miac/connect-linux')
    os.system('/opt/miac/connect.sh')

#запуск основого кода
class main:
    log_append("\nЗапуск кода")
    try:
        check_inventary_text() #Проверка на существоание inventory.txt и преобразование его в inventory.json
    except:
        pass

    create_json_info()  # Вызываем функцию проверки чтение данных компа и запись в json строка 32

    try:
        load_json_inventory() # Вызываем функцию проверка заполенния данных
    except:
        create_json_invetnory()
        application()  # Запск формы

    log_append("Отправка данных")

    connect()

if __name__ == "__main__":
    multiprocessing.freeze_support() #чтобы мультипроцессорность запретить (так надо для винды!!!)
    main()
