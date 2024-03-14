import json
import multiprocessing
import platform
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication

from other_file import check_inventar, log_append, newpath_file

multiprocessing.freeze_support()  # чтобы мультипроцессорность запретить (так надо для винды!!!)
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setFixedSize(800, 600)
        self.setWindowTitle("Инвентаризация АРМ")

        # Шрифты
        self.font11b = QtGui.QFont()
        self.font11b.setPointSize(11)
        self.font11b.setBold(True)
        self.font11b.setWeight(75)

        self.font20b = QtGui.QFont()
        self.font20b.setPointSize(20)
        self.font20b.setBold(True)
        self.font20b.setWeight(75)

        self.font9 = QtGui.QFont()
        self.font9.setPointSize(9)

        self.font9b = QtGui.QFont()
        self.font9b.setPointSize(9)
        self.font9b.setBold(True)
        self.font9b.setWeight(75)

        # Наполнение тела
        # Главная надпись
        self.lbl_name1 = QtWidgets.QLabel(self)
        self.lbl_name1.setText("Инвентаризация АРМ")
        self.lbl_name1.setGeometry(QtCore.QRect(0, 0, 800, 50))
        self.lbl_name1.setFont(self.font20b)
        self.lbl_name1.setAlignment(Qt.AlignCenter)

        self.lbl_name2 = QtWidgets.QLabel(self)
        self.lbl_name2.setText("медицинских организаций Чувашской Республики")
        self.lbl_name2.setGeometry(QtCore.QRect(0, 25, 800, 50))
        self.lbl_name2.setFont(self.font11b)
        self.lbl_name2.setAlignment(Qt.AlignCenter)

        self.lbl_name3 = QtWidgets.QLabel(self)
        self.lbl_name3.setText("В случае заполнения ложных данных станция будет отлючена от РМИС/МИС")
        self.lbl_name3.setGeometry(QtCore.QRect(0, 50, 800, 50))
        self.lbl_name3.setFont(self.font11b)
        self.lbl_name3.setAlignment(Qt.AlignCenter)
        self.lbl_name3.setStyleSheet("color : red")
        # Frame1
        self.frame_1 = QtWidgets.QFrame(self)
        self.frame_1.setGeometry(QtCore.QRect(10, 95, 781, 91))
        self.frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)

        self.lbl_tab1 = QtWidgets.QLabel(self.frame_1)
        self.lbl_tab1.setText('Информация о медицинской организации')
        self.lbl_tab1.setGeometry(QtCore.QRect(10, 10, 361, 17))
        self.lbl_tab1.setFont(self.font9b)

        # Наименование МО
        self.lbl_mo = QtWidgets.QLabel(self.frame_1)
        self.lbl_mo.setText("Медицинская организация: *")
        self.lbl_mo.setGeometry(QtCore.QRect(10, 30, 360, 20))
        self.lbl_mo.setFont(self.font9)

        self.chng_mo = QtWidgets.QComboBox(self.frame_1)
        self.chng_mo.setGeometry(QtCore.QRect(10, 50, 360, 25))
        self.chng_mo.setFont(self.font9)

        self.data_organization = ['Выберите медицинскую организацию',
                             'АУ "Городская стоматологическая поликлиника" Минздрава Чувашии',
                             'АУ "Новочебоксарская городская стоматологическая поликлиника" Минздрава Чувашии',
                             'АУ "Республиканская стоматологическая поликлиника" Минздрава Чувашии',
                             'АУ "Республиканский клинический онкологический диспансер" Минздрава Чувашии',
                             'АУ "Республиканский центр мануальной терапии" Минздрава Чувашии',
                             'БПОУ "Чебоксарский медицинский колледж" Минздрава Чувашии',
                             'БУ "Республиканская клиническая больница" Минздрава Чувашии',
                             'БУ "Республиканская клиническая офтальмологическая больница" Минздрава Чувашии',
                             'БУ "Республиканский клинический госпиталь для ветеранов войн" Минздрава Чувашии',
                             'БУ "Республиканский кожно-венерологический диспансер" Минздрава Чувашии',
                             'БУ "Республиканский наркологический диспансер" Минздрава Чувашии',
                             'БУ "Аликовская центральная районная больница" Минздрава Чувашии',
                             'БУ "Батыревская центральная районная больница" Минздрава Чувашии',
                             'БУ "Больница скорой медицинской помощи" Минздрава Чувашии',
                             'БУ "Вторая городская больница" Минздрава Чувашии',
                             'БУ "Вурнарская центральная районная больница" Минздрава Чувашии',
                             'БУ "Городская детская больница N 2" Минздрава Чувашии',
                             'БУ "Городская детская клиническая больница" Минздрава Чувашии',
                             'БУ "Городская клиническая больница N 1" Минздрава Чувашии',
                             'БУ "Городской клинический центр" Минздрава Чувашии',
                             'БУ "Ибресинская центральная районная больница" Минздрава Чувашии',
                             'БУ "Канашская центральная районная больница им. Ф.Г.Григорьева" Минздрава Чувашии',
                             'БУ "Канашский межтерриториальный медицинский центр" Минздрава Чувашии',
                             'БУ "Козловская центральная районная больница имени И.Е.Виноградова" Минздрава Чувашии',
                             'БУ "Комсомольская центральная районная больница" Минздрава Чувашии',
                             'БУ "Красночетайская районная больница" Минздрава Чувашии',
                             'БУ "Мариинско-Посадская центральная районная больница им. Н.А.Геркена" Минздрава Чувашии',
                             'БУ "Медицинский информационно-аналитический центр" Минздрава Чувашии',
                             'БУ "Моргаушская центральная районная больница" Минздрава Чувашии',
                             'БУ "Новочебоксарская городская больница" Минздрава Чувашии',
                             'БУ "Новочебоксарский медицинский центр" Минздрава Чувашии',
                             'БУ "Первая Чебоксарская городская больница имени Осипова Петра Николаевича - заслуженного врача РСФСР" Минздрава Чувашии',
                             'БУ "Президентский перинатальный центр" Минздрава Чувашии',
                             'БУ "Республиканская детская клиническая больница" Минздрава Чувашии',
                             'БУ "Республиканская психиатрическая больница" Минздрава Чувашии',
                             'БУ "Республиканская станция переливания крови" Минздрава Чувашии',
                             'БУ "Республиканский центр медицины катастроф и скорой медицинской помощи" Минздрава Чувашии',
                             'БУ "Республиканский детский санаторий "Лесная сказка" Минздрава Чувашии',
                             'БУ "Республиканский кардиологический диспансер" Минздрава Чувашии',
                             'БУ "Республиканский противотуберкулезный диспансер" Минздрава Чувашии',
                             'БУ "Республиканский центр по профилактике и борьбе со СПИД и инфекционными заболеваниями" Минздрава Чувашии',
                             'БУ "Республиканский центр общественного здоровья и медицинской профилактики, лечебной физкультуры и спортивной медицины" Минздрава Чувашии',
                             'БУ "Республиканское бюро судебно-медицинской экспертизы" Минздрава Чувашии',
                             'БУ "Урмарская центральная районная больница" Минздрава Чувашии',
                             'БУ "Центральная городская больница" Минздрава Чувашии',
                             'БУ "Центральная районная больница Алатырского района" Минздрава Чувашии',
                             'БУ "Цивильская центральная районная больница" Минздрава Чувашии',
                             'БУ "Чебоксарская районная больница" Минздрава Чувашии',
                             'БУ "Шемуршинская районная больница" Минздрава Чувашии',
                             'БУ "Шумерлинский межтерриториальный медицинский центр" Минздрава Чувашии',
                             'БУ "Ядринская центральная районная больница им. К.В.Волкова" Минздрава Чувашии',
                             'БУ "Яльчикская центральная районная больница" Минздрава Чувашии',
                             'БУ "Янтиковская центральная районная больница" Минздрава Чувашии',
                             'ГАУ ДПО "Институт усовершенствования врачей" Минздрава Чувашии',
                             'КУ "Республиканский детский противотуберкулезный санаторий "Чуварлейский бор" Минздрава Чувашии',
                             'КУ "Республиканский медицинский центр мобилизационных резервов "Резерв" Минздрава Чувашии',
                             'КУ "Специализированный Дом ребенка "Малютка" для детей с органическими поражениями центральной нервной системы с нарушением психики" Минздрава Чувашии',
                             'КУ "Центр ресурсного обеспечения государственных учреждений здравоохранения" Минздрава Чувашии']

        for item in self.data_organization:
            self.chng_mo.addItem(item)


        self.chng_mo.setCurrentIndex(0)  # Показываем по умолчанию
        self.bl_index1 = self.chng_mo.model()
        self.bl_index1.item(0).setEnabled(False)

        # Подразделение
        self.lbl_sp = QtWidgets.QLabel(self.frame_1)
        self.lbl_sp.setText('Структурное подразделение: *')
        self.lbl_sp.setGeometry(QtCore.QRect(410, 30, 360, 20))
        self.lbl_sp.setFont(self.font9)

        self.chng_sp = QtWidgets.QLineEdit(self.frame_1)
        self.chng_sp.setGeometry(QtCore.QRect(410, 50, 360, 25))
        self.chng_sp.setFont(self.font9)
        # self.chng_sp.addItem("Выберите структурное подразделение")
        # self.chng_sp.addItem("Поликлиника")
        # self.chng_sp.addItem("Стационар")
        # self.chng_sp.addItem("ОВОП")
        # self.chng_sp.addItem("ВА")
        # self.chng_sp.addItem("ФАП")
        # self.chng_sp.addItem("")
        # self.chng_sp.addItem("")
        # self.chng_sp.setCurrentIndex(0)  # Показываем по умолчанию
        # self.bl_index = self.chng_sp.model()
        # self.bl_index.item(0).setEnabled(False)

        # Frame2
        self.frame_2 = QtWidgets.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(10, 200, 380, 341))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)

        self.lbl_tab2 = QtWidgets.QLabel(self.frame_2)
        self.lbl_tab2.setText('Адрес установки')
        self.lbl_tab2.setGeometry(QtCore.QRect(10, 10, 361, 17))
        self.lbl_tab2.setFont(self.font9b)

        # Регион
        self.lbl_region = QtWidgets.QLabel(self.frame_2)
        self.lbl_region.setText('Регион: *')
        self.lbl_region.setGeometry(QtCore.QRect(10, 30, 360, 20))
        self.lbl_region.setFont(self.font9)


        self.lbl_name3 = QtWidgets.QLabel(self)
        self.lbl_name3.setText("В случае заполнения ложных данных станция будет отлючена от РМИС/МИС")
        self.lbl_name3.setGeometry(QtCore.QRect(0, 50, 800, 50))
        self.lbl_name3.setFont(self.font11b)
        self.lbl_name3.setAlignment(Qt.AlignCenter)
        self.lbl_name3.setStyleSheet("color : red")

        self.chng_region = QtWidgets.QLineEdit(self.frame_2)
        self.chng_region.setGeometry(QtCore.QRect(10, 50, 360, 25))
        self.chng_region.setFont(self.font9)
        self.chng_region.setText('Чувашская Республика')
        # Район
        self.lbl_rayon = QtWidgets.QLabel(self.frame_2)
        self.lbl_rayon.setText('Район:')
        self.lbl_rayon.setGeometry(QtCore.QRect(10, 80, 360, 20))
        self.lbl_rayon.setFont(self.font9)

        self.chng_rayon = QtWidgets.QLineEdit(self.frame_2)
        self.chng_rayon.setGeometry(QtCore.QRect(10, 100, 360, 25))
        self.chng_rayon.setFont(self.font9)
        # Населеный пункт
        self.lbl_city = QtWidgets.QLabel(self.frame_2)
        self.lbl_city.setText('Населеный пункт: *')
        self.lbl_city.setGeometry(QtCore.QRect(10, 130, 360, 20))
        self.lbl_city.setFont(self.font9)

        self.chng_city = QtWidgets.QLineEdit(self.frame_2)
        self.chng_city.setGeometry(QtCore.QRect(10, 150, 360, 25))
        self.chng_city.setFont(self.font9)
        # Улица
        self.lbl_ulica = QtWidgets.QLabel(self.frame_2)
        self.lbl_ulica.setText('Улица/Пр-кт/Площадь: *')
        self.lbl_ulica.setGeometry(QtCore.QRect(10, 180, 360, 20))
        self.lbl_ulica.setFont(self.font9)

        self.chng_ulica = QtWidgets.QLineEdit(self.frame_2)
        self.chng_ulica.setGeometry(QtCore.QRect(10, 200, 360, 25))
        self.chng_ulica.setFont(self.font9)
        # Дом
        self.lbl_dom = QtWidgets.QLabel(self.frame_2)
        self.lbl_dom.setText('Дом: *')
        self.lbl_dom.setGeometry(QtCore.QRect(10, 230, 170, 20))
        self.lbl_dom.setFont(self.font9)

        self.chng_dom = QtWidgets.QLineEdit(self.frame_2)
        self.chng_dom.setGeometry(QtCore.QRect(10, 250, 170, 25))
        self.chng_dom.setFont(self.font9)

        # Корпус
        self.lbl_korpus = QtWidgets.QLabel(self.frame_2)
        self.lbl_korpus.setText('Корпус:')
        self.lbl_korpus.setGeometry(QtCore.QRect(200, 230, 170, 20))
        self.lbl_korpus.setFont(self.font9)

        self.chng_korpus = QtWidgets.QLineEdit(self.frame_2)
        self.chng_korpus.setGeometry(QtCore.QRect(200, 250, 170, 25))
        self.chng_korpus.setFont(self.font9)

        # Кабинет
        self.lbl_kab = QtWidgets.QLabel(self.frame_2)
        self.lbl_kab.setText('Кабинет: *')
        self.lbl_kab.setGeometry(QtCore.QRect(10, 280, 170, 20))
        self.lbl_kab.setFont(self.font9)

        self.chng_kab = QtWidgets.QLineEdit(self.frame_2)
        self.chng_kab.setGeometry(QtCore.QRect(10, 300, 170, 25))
        self.chng_kab.setFont(self.font9)

        # Индекс
        self.lbl_index = QtWidgets.QLabel(self.frame_2)
        self.lbl_index.setText('Почтовый индекс: ')
        self.lbl_index.setGeometry(QtCore.QRect(200, 280, 170, 20))
        self.lbl_index.setFont(self.font9)

        self.chng_index = QtWidgets.QLineEdit(self.frame_2)
        self.chng_index.setGeometry(QtCore.QRect(200, 300, 170, 25))
        self.chng_index.setFont(self.font9)

        # Frame3
        self.frame_3 = QtWidgets.QFrame(self)
        self.frame_3.setGeometry(QtCore.QRect(400, 200, 391, 341))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)

        self.lbl_frame3 = QtWidgets.QLabel(self.frame_3)
        self.lbl_frame3.setText('Информация о АРМ')
        self.lbl_frame3.setGeometry(QtCore.QRect(10, 10, 361, 17))
        self.lbl_frame3.setFont(self.font9b)

        # Инвентарный номер
        self.lbl_invent_n = QtWidgets.QLabel(self.frame_3)
        self.lbl_invent_n.setText('Инвентарный номер: *')
        self.lbl_invent_n.setGeometry(QtCore.QRect(10, 80, 161, 20))
        self.lbl_invent_n.setFont(self.font9)

        self.chng_invent_n = QtWidgets.QLineEdit(self.frame_3)
        self.chng_invent_n.setGeometry(QtCore.QRect(179, 80, 200, 25))
        self.chng_invent_n.setFont(self.font9)

        # Серийный номер
        self.lbl_ser_n = QtWidgets.QLabel(self.frame_3)
        self.lbl_ser_n.setText('Серийны номер: *')
        self.lbl_ser_n.setGeometry(QtCore.QRect(10, 40, 161, 20))
        self.lbl_ser_n.setFont(self.font9)

        self.chng_ser_n = QtWidgets.QLineEdit(self.frame_3)
        self.chng_ser_n.setGeometry(QtCore.QRect(179, 40, 200, 25))
        self.chng_ser_n.setFont(self.font9)
        # год ввода в экспл.
        self.lbl_year = QtWidgets.QLabel(self.frame_3)
        self.lbl_year.setText('Год ввода в эксплуатацию: *')
        self.lbl_year.setGeometry(QtCore.QRect(10, 120, 165, 20))
        self.lbl_year.setFont(self.font9)

        self.chng_year = QtWidgets.QLineEdit(self.frame_3)
        self.chng_year.setGeometry(QtCore.QRect(180, 120, 201, 25))
        self.chng_year.setFont(self.font9)

        self.lbl_wan = QtWidgets.QLabel(self.frame_3)
        self.lbl_wan.setText('Тип WAN подключения: *')
        self.lbl_wan.setGeometry(QtCore.QRect(10, 160, 161, 20))
        self.lbl_wan.setFont(self.font9)

        self.chng_wan = QtWidgets.QComboBox(self.frame_3)
        self.chng_wan.setGeometry(QtCore.QRect(180, 160, 201, 25))
        self.chng_wan.setFont(self.font9)
        #
        # self.chng_wan.addItem("Выберите тип подключения")
        # self.chng_wan.addItem("оптика")
        # self.chng_wan.addItem("медь")
        # self.chng_wan.addItem("ADSL")
        # self.chng_wan.addItem("Мобильный интернет")
        # self.chng_wan.addItem("Спутниковый интернет")
        # self.chng_wan.addItem("Wi-Fi")
        # self.chng_wan.addItem("Wi-Max")
        # self.chng_wan.setCurrentIndex(0)  # Показываем по умолчанию
        # self.bl_index = self.chng_wan.model()
        # self.bl_index.item(0).setEnabled(False)

        self.data_wan = ["Выберите тип подключения", "оптика", 'медь', 'ADSL', 'Мобильный интернет',
                         'Спутниковый интернет', 'Wi-Fi', 'Wi-Max']
        for item in self.data_wan:
            self.chng_wan.addItem(item)

        self.chng_wan.setCurrentIndex(0)  # Показываем по умолчанию
        self.bl_index = self.chng_wan.model()
        self.bl_index.item(0).setEnabled(False)

        # Ок
        self.btn_ok = QtWidgets.QPushButton(self)
        self.btn_ok.setText('Cохранить данные')
        self.btn_ok.setGeometry(QtCore.QRect(335, 555, 120, 25))
        self.btn_ok.setToolTip("Cохранить данные")
        self.btn_ok.clicked.connect(self.write_file)


        self.zvezdochka = QtWidgets.QLabel(self)
        self.zvezdochka.setText('* - Поля обязательные для заполнения')
        self.zvezdochka.setGeometry(QtCore.QRect(30, 540, 250, 25))
        self.zvezdochka.setFont(self.font9)
        self.zvezdochka.setStyleSheet("color : red")


        self.find_file_text()

    def replace(self,texts):
        texts = texts.replace('Медицинская организация:', '').replace('Регион:', '').replace('Район:', '').replace('Населенный пункт:', '').replace('Корпус:', '').replace('Дом:', '').replace('Улица/Пр-кт/Площадь:', '').replace('Структурное подразделение:', '').replace('Почтовый индекс:', '').replace('Кабинет:', '').replace('Тип подключения:', '').replace('Год ввода в эксплуатацию:', '').replace('Серийный номер:', '').replace('Инвентраный номер:', '')
        return texts
    def find_file_text(self,):
        try:
            with open(str(check_inventar()[1])) as json_file:
                data = json.load(json_file)
                for p in data['Form info']:
                    for j,i in enumerate(self.data_organization):
                        if i.find(p['Медицинская организация']) >= 0:
                            self.chng_mo.setCurrentIndex(j)
                            break

                    for j, i in enumerate(self.data_wan):
                        if i.find(p['Тип подключения']) >= 0:
                            self.chng_wan.setCurrentIndex(j)
                            break
                    self.chng_rayon.setText(p['Район'])
                    self.chng_region.setText(p['Регион'])
                    self.chng_city.setText(p['Населенный пункт'])
                    self.chng_ulica.setText(p['Улица/Пр-кт/Площадь'])
                    self.chng_dom.setText(p['Дом'])
                    self.chng_korpus.setText(p['Корпус'])
                    self.chng_kab.setText(p['Кабинет'])
                    self.chng_index.setText(p['Почтовый индекс'])
                    self.chng_sp.setText(p['Структурное подразделение'])
                    self.chng_invent_n.setText(p['Инвентраный номер'])
                    self.chng_ser_n.setText(p['Серийный номер'])
                    self.chng_year.setText(p['Год ввода в эксплуатацию'])
        except:
                self.chng_rayon.setText('')
                self.chng_city.setText('')
                self.chng_ulica.setText('')
                self.chng_dom.setText('')
                self.chng_korpus.setText('')
                self.chng_kab.setText('')
                self.chng_index.setText('')
                self.chng_sp.setText('')
                self.chng_invent_n.setText('')
                self.chng_ser_n.setText('')
                self.chng_year.setText('')
                self.chng_mo.setCurrentIndex(0)
                self.chng_wan.setCurrentIndex(0)


    def write_file(self):
        if self.chng_mo.currentText() == 'Выберите медицинскую организацию':
            self.error_write()
        elif self.chng_region.text() == '':
            self.error_write()
        elif self.chng_ulica.text() == '':
            self.error_write()
        elif self.chng_dom.text() == '':
            self.error_write()
        elif self.chng_kab.text() == '':
            self.error_write()
        elif self.chng_sp.text() == '':
            self.error_write()
        elif self.chng_invent_n.text() == '':
            self.error_write()
        elif self.chng_ser_n.text() == '':
            self.error_write()
        elif self.chng_wan.currentText() == 'Выберите тип подключения':
            self.error_write()
        else:
            #################  узнаем версию системы и от нее пляшем #################
            data = {}
            data['Form info'] = []
            data['Form info'].append({
                'Медицинская организация': self.chng_mo.currentText(),
                'Регион': self.chng_region.text(),
                'Район': self.chng_rayon.text(),
                'Населенный пункт': self.chng_city.text(),
                'Улица/Пр-кт/Площадь': self.chng_ulica.text(),
                'Дом': self.chng_dom.text(),
                'Корпус': self.chng_korpus.text(),
                'Кабинет': self.chng_kab.text(),
                'Почтовый индекс': self.chng_index.text(),
                'Структурное подразделение': self.chng_sp.text(),
                'Инвентраный номер': self.chng_invent_n.text(),
                'Серийный номер': self.chng_ser_n.text(),
                'Год ввода в эксплуатацию': self.chng_year.text(),
                'Тип подключения': self.chng_wan.currentText()
            })
            with open(str(check_inventar()[1]), 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=4)
            self.good_write()

    def error_write(self):
        error = QMessageBox()
        error.setWindowTitle('Ошибка!!!')
        error.setText('Заполнены не все обязательные поля')
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Close)
        error.exec_()

    def good_write(self):
        log_append('Данные в форму записаны успешно')
        good = QMessageBox()
        good.setWindowTitle('Успешно')
        good.setText('Данные записаны успешно')
        # good.setIcon(QMessageBox.Accepted)
        good.exec_()
        self.close()


def application():
    log_append('Запуск формы заполнения данных')
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    app.exec_()


if __name__ == "__main__":
    application()

