#import windows_tools.antivirus
#from windows_tools.installed_software import get_installed_software
#import winapps
#import winreg
#import wmi
import multiprocessing
import subprocess
from other_file import message, log_append

multiprocessing.freeze_support()  # чтобы мультипроцессорность запретить (так надо для винды!!!)

####### библиротека windows #######
def windows_antivirus_all():
    try:
        # проверка антивируса #1
        from windows_tools.installed_software import get_installed_software
        data_antivirus = ['kasper', 'dr.web']
        d_antivirs = []
        for software in get_installed_software():
            soft_name = str(software['name'])
            if soft_name:
                for item in data_antivirus:  # перебор списка с антивирусами
                    if item in soft_name.lower():  # поиск совпадений в ОС
                        proc = ''
                        if item == 'kasper':
                            proc = str(process_kasper())
                        if item == 'dr.web':
                            proc = str(process_dr_web())
                        proc = ''.join(proc.split())
                        print(str(proc))
                        text = str(soft_name)+' v.'+str(software["version"])+' Процесс: '+str(proc)
                        print(text)
                        d_antivirs.append(text)
        antivirus = ''.join(d_antivirs)
        #
        if not d_antivirs:
            antivirus = "Не установлен"
    except:
        antivirus = ''
    return antivirus


# ############################ реестр software ################################
# # поиск названия антивируса в реестре software
# def find_softdir_antivirus():
#     antivirus = []
#     name_dr_web = 'DOCTOR'
#     output = subprocess.check_output(['reg', 'query', r'HKLM\SOFTWARE']).decode('utf-8') #декодирует с cmd полученные результаты
#     for i in output.split('\n'): #перебор полученных данных
#         i = (str(i).replace(r'HKEY_LOCAL_MACHINE\SOFTWARE\  '.replace('  ', ''), '')).upper().replace('\r', '') # удляет пробелы,ненужные елементы и делает в верхний регистр
#         if i.find(name_dr_web.upper()) >= 0:
#             antivirus.append(str(i))
#     antivirus = ''.join(antivirus)
#     return antivirus


# #поиск названия антивируса kasper
# def kasper_reestr():
#     try:
#         # запускаем команду с параметрами и получаем вывод
#         output = subprocess.check_output(['reg', 'query', r'HKLM\SOFTWARE\KASPERSKY\SETUP'])
#         # преобразуем вывод в строку
#         output_str = output.decode('utf-8')
#         # парсим вывод и получаем значения
#         values = str(output_str.split('\\')[len(output_str.split('\\')) - 1]).replace(r'\r\n', '')
#     except:
#         values = ''
#     return values


# проверка в реестре по назанию ключа и значения в версию
def search_registry(key, value): 
    reg_handle = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    reg_key = winreg.OpenKey(reg_handle, key)
    result = winreg.QueryValueEx(reg_key, value)[0]
    return result


# поиск названия антивируса drweb
def find_dr_web_dir_reestr():
    # запускаем команду с параметрами и получаем вывод
    x = (r'HKLM\SOFTWARE\DOCTOR WEB\SETUP').replace('  ', '')
    output = subprocess.check_output(['reg', 'query', x])
    # преобразуем вывод в строку
    output_str = output.decode('utf-8')
    # парсим вывод и получаем значения
    values = str(output_str.split('\\')[len(output_str.split('\\')) - 1]).replace(r'\r\n', '')
    return values


# проецсс drweb
def process_dr_web():
    porcess_program = 'False'
    try:
        f = wmi.WMI()
        for i in f.Win32_Process():
            proc = str(i.Name).lower()
            if proc.find('dwservice.exe') >= 0 or proc.find('spideragent.exe') >= 0:
                porcess_program = 'True'
    except Exception as e:
        errors = "Проблема в поиске процесса. Ошибка: " + str(e)
        print(errors)
        log_append(errors)
        porcess_program = 'False'
    return porcess_program


# процес каспер
def process_kasper():
    porcess_program = 'False'
    try:
        f = wmi.WMI()
        for i in f.Win32_Process():
            proc = str(i.Name).lower()
            if proc.find('avp.exe') >= 0 or proc.find('kavsf.exe') >= 0:
                porcess_program =  'True'
    except Exception as e:
        errors = "Проблема в поиске процесса. Ошибка: " + str(e)
        print(errors)
        log_append(errors)
        porcess_program = 'False Program'
    return porcess_program



# сбор всех данных
def start_search():
    antivirus = ''
    try:
        name = ' '.join((str(find_dr_web_dir_reestr()).replace('\n', '').upper()).split())
        url = (r'SOFTWARE\DOCTOR WEB\SETUP\  ' + name + r'\SETTINGS').replace('  ', '')
        version = search_registry(url, "SETUPVERSION")
        antivirus = str(name)+'  v.'+str(version)+' Процесc:'+str(process_dr_web())
        log_append('в реестре найден dr web')
        return antivirus
    except:
        pass



    try:
        url = (r'SOFTWARE\KasperskyLab\protected\AVP9\environment').replace('  ', '')
        name = search_registry(url, "PRODUCTNAME")
        version = search_registry(url, "PRODUCTVERSION")
        antivirus = str(name)+'  v.'+str(version)+' Процесc:'+str(process_kasper())
        log_append('в реестре найден kasper х32 AVP9')
        return antivirus
    except:
        try:
            url = (r'SOFTWARE\KasperskyLab\protected\KES\environment').replace('  ', '')
            name = search_registry(url, "PRODUCTNAME")
            version = search_registry(url, "PRODUCTVERSION")
            antivirus = str(name)+'  v.'+str(version)+' Процесc:'+str(process_kasper())
            log_append('в реестре найден kasper х32 KES')
            return antivirus
        except:
            pass

    try:
        url = (r'SOFTWARE\Wow6432Node\KasperskyLab\protected\AVP9\environment').replace('  ', '')
        name = search_registry(url, "PRODUCTNAME")
        version = search_registry(url, "PRODUCTVERSION")
        antivirus = str(name)+'  v.'+str(version)+' Процесc:'+str(process_kasper())
        log_append('в реестре найден kasper х64 AVP9')
        return antivirus
    except:
        try:
            url = (r'SOFTWARE\Wow6432Node\KasperskyLab\protected\KES\environment').replace('  ', '')
            name = search_registry(url, "PRODUCTNAME")
            version = search_registry(url, "PRODUCTVERSION")
            antivirus = str(name)+'  v.'+str(version)+' Процесc:'+str(process_kasper())
            log_append('в реестре найден kasper x64 KES')
            return antivirus
        except:
            pass

    if antivirus == '':
        antivirus = str(windows_antivirus_all())
        log_append('Антивирус найден через библиотку')

    return antivirus


def windows_antivirus():
    antivirus = str(start_search())
    print(antivirus)
    log_append(antivirus)
    return antivirus

# windows_antivirus()



