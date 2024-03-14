import json
import multiprocessing
import os
import platform
import subprocess
from other_file import message, close_program, log_append

multiprocessing.freeze_support()  # чтобы мультипроцессорность запретить (так надо для винды!!!)
newpath_file = 'inventory.txt'  # название файла инвентаризации
newpath_file_json = 'inventory.json'  # название файла инвентаризации


def check_inventars():
    # проверка имени системы
    if platform.system() == "Windows":
        try:
            newpath_windows = r'C:/miac/inventory/'
        except:
            dir_catalog = (str(os.path.abspath(__file__)))  # текущая директория
            dir_name_disk = (dir_catalog[0: dir_catalog.index(":")])  # с какого имени диска был запущен файл
            newpath_windows = r'' + dir_name_disk + ':/miac/inventory/'
        newpath = newpath_windows
    else:
        newpath = '/opt/miac/inventory/'

    # проверяет папку если нет то созадет при условии что /opt/ имеет права 777
    if not os.path.exists(newpath):
        try:
            os.makedirs(newpath)
        except:
            message('Не удалось создать папку в корне каталога')
            close_program()

    result = os.path.exists(os.path.join(os.getcwd(), newpath,
                                         newpath_file))  # проверка на существ файла newpath-это путь newpath_file-это файл
    result_dir = str(newpath + newpath_file)
    # result - проверка файла
    # result_dir - путь с указанием файла напирмер /opt/miac/inventory/inventiry.txt
    # newpath - путь до файла
    return result, result_dir, newpath

def check_inventary_text():
    if check_inventars()[0]:
        log_append("\nПреобразование inventory.txt в inventory.json")
        print(check_inventars()[0])
        # чтение файла инветраизации на локльном компе
        with open(str(check_inventars()[1]), 'r', -1, 'utf-8') as f:
            readlines = f.readlines()

        ### сделано именно так, потому что на некторых компах есть уже
        ### в /opt/miac/ инвентарзиационные текстовый документа inventory.txt
        ### проишлось сделать так

        category = ['Медицинская организация', 'Регион', 'Район', 'Населенный пункт',
                    'Улица/Пр-кт/Площадь', 'Дом', 'Корпус', 'Кабинет', 'Почтовый индекс',
                    'Структурное подразделение', 'Инвентраный номер', 'Серийный номер',
                    'Год ввода в эксплуатацию', 'Тип подключения']
        organization = readlines[0].replace('\n', '').replace(category[0] + ':', '')  # Медицинская организация
        region = readlines[1].replace('\n', '').replace(category[1] + ':', '')  # Регион
        district = readlines[2].replace('\n', '').replace(category[2] + ':', '')  # Район
        locality = readlines[3].replace('\n', '').replace(category[3] + ':', '')  # Населенный пункт
        street = readlines[4].replace('\n', '').replace(category[4] + ':', '')  # Улица/Пр-кт/Площадь
        house = readlines[5].replace('\n', '').replace(category[5] + ':', '')  # Дом
        housing = readlines[6].replace('\n', '').replace(category[6] + ':', '')  # Корпус
        cabinet = readlines[7].replace('\n', '').replace(category[7] + ':', '')  # Кабинет
        postcode = readlines[8].replace('\n', '').replace(category[8] + ':', '')  # Почтовый индекс
        structural_subdivision = readlines[9].replace('\n', '').replace(category[9] + ':',
                                                                        '')  # Структурное подразделение
        inventory_number = readlines[10].replace('\n', '').replace(category[10] + ':', '')  # Инвентраный номер
        serial_number = readlines[11].replace('\n', '').replace(category[11] + ':', '')  # Серийный номер
        year_of_commissioning = readlines[12].replace('\n', '').replace(category[12] + ':',
                                                                        '')  # Год ввода в эксплуатацию
        connection_type = readlines[13].replace('\n', '').replace(category[13] + ':', '')  # Тип подключения

        data = {}
        data['Form info'] = []
        data['Form info'].append(
            {'Медицинская организация': organization, 'Регион': region, 'Район': district, 'Населенный пункт': locality,
             'Улица/Пр-кт/Площадь': street, 'Дом': house,
             'Корпус': housing, 'Кабинет': cabinet, 'Почтовый индекс': postcode,
             'Структурное подразделение': structural_subdivision,
             'Инвентраный номер': inventory_number, 'Серийный номер': serial_number,
             'Год ввода в эксплуатацию': year_of_commissioning,
             'Тип подключения': connection_type
             })
        with open(str(check_inventars()[2] + newpath_file_json), 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

        os.remove(str(check_inventars()[1]))
