import multiprocessing
import os
import platform
# from easygui import *
import sys
from time import gmtime, strftime


multiprocessing.freeze_support()  # чтобы мультипроцессорность запретить (так надо для винды!!!)
newpath_file = 'inventory.json' #название файла инвентаризации
newpath_file_info = 'info.json' #название файла инвентаризации

def data():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


########## форма ##########
#существовние файла инвентаризации в папке linux

def check_inventar():
    #проверка имени системы
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


    result = os.path.exists(os.path.join(os.getcwd(), newpath, newpath_file)) #проверка на существ файла newpath-это путь newpath_file-это файл
    result_dir = str(newpath+newpath_file)
    result_info = os.path.exists(os.path.join(os.getcwd(), newpath, newpath_file_info)) #проверка на существ файла newpath-это путь newpath_file-это файл
    result_dir_info = str(newpath+newpath_file_info)
    #result - проверка файла
    # result_dir - путь с указанием файла напирмер /opt/miac/inventory/inventiry.txt
    # newpath - путь до файла
    return result,result_dir,newpath,result_dir_info



def log_append(text):
    url = check_inventar()[2]+'log.txt'
    with open(url, 'a') as outfile:
        outfile.write(data() + " " + str(text) + "\n")
def close_program():
    sys.exit()



########## сообщения ##########
def message(message):
    try:
        if platform.system()  == "Windows":
            title = "Уведомление"
            ok_btn_txt = "Закрыть"
            msgbox(message, title, ok_btn_txt)
        else:
            os.system('DISPLAY=:0 notify-send "' + message + '" -t 65000') #уведомление в linux
    except:
        log_append('Ошибка отправки увеомления')
    return



# шифрование
class Main:
    def spl(self, x, encoding='utf-8', errors='surrogatepass'):
        n = int(x, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

