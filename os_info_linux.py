import multiprocessing
import os
import subprocess

multiprocessing.freeze_support()  # чтобы мультипроцессорность запретить (так надо для винды!!!)
#антивирусы
def linux_antivirus():
    try:
        antivirus = str(subprocess.check_output('drweb-ctl -v', shell=True))
        try:
            licenses = str(subprocess.check_output('drweb-ctl license', shell=True))
            antivirus = antivirus + " / Лицензия - " + licenses
        except:
            antivirus = antivirus + " / " + "Нет лицензии"
        antivirus = antivirus.replace("b'", "").replace("'", "").replace("\\n", "") # удаление хлама
    except:
        try:
            command = "kesl-control --app-info"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            if error:
                return "Ошибка при выполнении команды"
            else:
                items = output.decode("utf-8").split()
                antivirus_name = items.index("Название:")
                name = " ".join([items[i] for i in range(antivirus_name + 1, antivirus_name + 4)])

                versions_index = items.index("Версия:")
                version = items[versions_index + 1]
                print(version)
                antivirus = name + " v." + version
        except OSError:
            antivirus = 'Не установлен'
    return antivirus


#wine
def linux_wine():
    ####### linux #######

    try:
        wine = str(subprocess.check_output('wine --version', shell=True))
        wine = wine.replace("b'", "").replace("'", "").replace("\\n", "") # удаление хлама
    except:
        wine = 'Не установлен'
    return wine


#Secret NET
def linux_secret_net():
    try:
        secret_net = str(subprocess.check_output('cat /opt/secretnet/etc/secretnet-release', shell=True))
        try:
            secret_net_licensce = str(subprocess.check_output('sudo /opt/secretnet/bin/snlicensectl -s', shell=True))
            if secret_net_licensce:
                secret_net = secret_net + ' / Лицензии Есть'
        except:
            secret_net = secret_net + ' / Лицензии НЕТ '
        secret_net = secret_net.replace("b'", "").replace("'", "").replace("\\n", "") # удаление хлама

    except:
        secret_net = "Не установлен"
    return secret_net

