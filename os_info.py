import multiprocessing
import os
import subprocess
import psutil
from cpuinfo import cpuinfo
from getmac import getmac
import platform
import socket
from form import application
from os_info_linux import linux_antivirus, linux_wine, linux_secret_net
from os_info_windows import windows_antivirus
from other_file import check_inventar, log_append, message

multiprocessing.freeze_support()  # чтобы мультипроцессорность запретить (так надо для винды!!!)



#узнаем ip
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #запрос через сокет
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('192.168.92.20', 1)) #подключение
        IP = s.getsockname()[0] #вывод
    except Exception:
        IP = 'Не доступен'
    finally:
        s.close()
    return IP




# Функция конвертирования данных памяти
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            x ="%.2f" % bytes+unit+suffix
            return x
        bytes /= factor




#достает все данные из компа
def os_files():

    log_append('Чтение данных о компе и ПО')
    uname = platform.uname() #все данные
    name = uname.node  # имя пользователя


    #имя ОС
    try:
        node_name = str(uname.system)
    except:
        a = (str(subprocess.check_output('lsb_release -a', shell=True)).replace("b\'", '').replace(r"\t", "").replace(
            r"\n", ";").replace("Distributor ID:", "").replace("Codename:", "").replace("Description:", "")).split(';')
        node_name = a[0]


    # релиз
    try:
        release = str(uname.release)
    except:
        a = (str(subprocess.check_output('lsb_release -a', shell=True)).replace("b\'", '').replace(r"\t", "").replace(
            r"\n", ";").replace("Distributor ID:", "").replace("Codename:", "").replace("Description:", "")).split(';')
        release = a[1]


    # antivirus

    if platform.system() == "Windows":
        antivirus = windows_antivirus()
    else:
        antivirus = linux_antivirus()


    if platform.system() == "Windows":
        wine = '-'
        secret_net = '-'
    else:
        wine = linux_wine() # wine linux
        secret_net = linux_secret_net()# secret net linux

    processor_info = cpuinfo.get_cpu_info()['brand_raw']  # инфа процессора
    cores = str(psutil.cpu_count(logical=False))  +'/'+ str(psutil.cpu_count(logical=True) ) +'/'+ get_size(psutil.virtual_memory().total) # ФИЗ.. ЯДЕР / ВСЕГО ЯДЕР / ОПЕРАТИ.. ПАМЯТЬ
    memory = get_size(psutil.disk_usage(os.sep).total) +'/'+ get_size(psutil.disk_usage(os.sep).free) #ОБЪЕМ ДИСКА /  СВОБО.. ОБЪЕМ

    ip = get_ip() #ip
    mac = getmac.get_mac_address()  #мак
    release = release  #версия ОС
    node_name = node_name  #имя OC
    name = name #имя



    return name,ip,mac,node_name,release,antivirus,wine,secret_net,processor_info,cores,memory
