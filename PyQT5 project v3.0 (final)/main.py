# Импортируем необходимые нам библиотеки
import sys
import mysql.connector
from string import digits, ascii_letters, punctuation

from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit


# Функции для работы с базой данных принимающие в качестве аргумента SQL запрос
# Функция возвращающая выбранные элементы из бд
def select(query):
    con = mysql.connector.connect(host='sql11.freesqldatabase.com',
                                  user='sql11661411',
                                  password='qfts8vCfIb',
                                  database='sql11661411',
                                  charset='utf8')
    cur = con.cursor()
    cur.execute(*query)
    result = cur.fetchall()
    con.close()
    return result


# Функция для занесенния новых данных в бд
def insert(query):
    con = mysql.connector.connect(host='sql11.freesqldatabase.com',
                                  user='sql11661411',
                                  password='qfts8vCfIb',
                                  database='sql11661411',
                                  charset='utf8')
    cur = con.cursor()
    cur.execute(*query)
    con.commit()
    con.close()


# Класс окна регистрации
class Registration(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('registration_window.ui', self)

        # Объявление переменных отвечающих за видимость паролей
        self.password_hide = True
        self.pwd_check_hide = True

    # Установка интерфейса
    def initUI(self):
        self.setWindowTitle('Yandex_lyceum')

        # Первоначальное значение True переменных означающее что пароль скрыт
        self.password_hide = True
        self.pwd_check_hide = True

        # Первоначальная установка пустого текста в полях ввода
        self.surname.setText('')
        self.name.setText('')
        self.login.setText('')
        self.password.setText('')
        self.pwd_check.setText('')

        # Первоначальная установка скрытого стиля пароля
        self.password.setEchoMode(QLineEdit.Password)
        self.pwd_check.setEchoMode(QLineEdit.Password)

        # Обрабатываем нажатия на кнопки
        self.registration_button.clicked.connect(self.registration)

        self.back_button.clicked.connect(self.back)

        self.style_password_button.clicked.connect(self.style_password)
        self.style_pwd_check_button.clicked.connect(self.style_pwd_check)

        # Задаем стиль заголовка
        self.registration_label.setFont(QFont("Times", 15, QFont.Bold))

        # Задаем стиль текста и первоначальную скрытность текста ошибок
        self.error_check1.hide()
        self.error_check2.hide()
        self.error_login.hide()
        self.error_surname.hide()
        self.error_name.hide()
        self.error.hide()
        self.error_check1.setStyleSheet("color: red;")
        self.error_check2.setStyleSheet("color: red;")
        self.error_login.setStyleSheet("color: red;")
        self.error_surname.setStyleSheet("color: red;")
        self.error_name.setStyleSheet("color: red;")
        self.error.setStyleSheet("color: red;")

    # Функция отвечающая за регистрацию нового пользователя в бд
    def registration(self):
        if self.password.text() == self.pwd_check.text()\
                and self.check_password(self.password.text())\
                and not self.check_login(self.login.text)\
                and self.name.text() and self.surname.text()\
                and self.login.text():
            # Заносим информацию о пользователе в бд если все поля текста заполнены
            insert([f"""INSERT INTO Users VALUES 
            ('{self.login.text()}',
            '{self.surname.text()}',
            '{self.name.text()}',
            '{self.password.text()}')"""])

            # Переходим на экран входа
            registration.close()
            login.initUI()
            login.show()

        # Отображения ошибок в случае некорректности введенных данных пользователя
        self.error_check1.show() if self.password.text() != self.pwd_check.text() else self.error_check1.hide()
        self.error_check2.show() if not self.check_password(self.password.text()) else self.error_check2.hide()
        self.error_login.show() if self.check_login(self.login.text()) else self.error_login.hide()
        self.error_name.show() if not self.name.text() else self.error_name.hide()
        self.error_surname.show() if not self.surname.text() else self.error_surname.hide()
        self.error.show() if not self.login.text() else self.error.hide()

    # Проверка пароля на безопасность
    def check_password(self, pwd):
        return len(pwd) >= 8 and\
            any(list(filter(lambda x: x in digits, pwd)))\
            and any(list(filter(lambda x: x in ascii_letters, pwd)))\
            and any(list(filter(lambda x: x in punctuation, pwd)))

    # Проверка на уникальность логина в бд
    def check_login(self, login):
        logins = [item[0] for item in select(["SELECT login from Users"])]
        return login in logins

    # Функция возвращающая пользователя на экран входа по нажатию кноки
    def back(self):
        registration.close()
        login.initUI()
        login.show()

    # Функции меняющие видимость паролей
    def style_password(self):
        if self.password_hide:
            self.password.setEchoMode(QLineEdit.Normal)
            self.password_hide = False
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.password_hide = True

    def style_pwd_check(self):
        if self.pwd_check_hide:
            self.pwd_check.setEchoMode(QLineEdit.Normal)
            self.pwd_check_hide = False
        else:
            self.pwd_check.setEchoMode(QLineEdit.Password)
            self.pwd_check_hide = True


# Класс окна входа
class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('start_window.ui', self)

        # Объявление переменной отвечающей за видимость пароля
        self.password_hide = True

        self.initUI()

    # Устанавливаем интерфейс
    def initUI(self):
        self.setWindowTitle('Yandex_lyceum')

        # Первоначальная установка пустых полей ввода
        self.login_text.setText('')
        self.password_text.setText('')

        # Первоначальная установка скрытого пароля
        self.password_text.setEchoMode(QLineEdit.Password)

        # Стиль заголовка
        self.title.setFont(QFont("Times", 10, QFont.Bold))

        # Видимость и цвет ошибок
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        # Обрабатываем нажатия на кнопки
        self.sign_in_button.clicked.connect(self.sign_in)

        self.registration_button.clicked.connect(self.registration)

        self.style_password_button.clicked.connect(self.style_password)

    # Функция для входа пользователя в почту
    def sign_in(self):
        data = select(["SELECT login, password from Users"])
        if (self.login_text.text(), self.password_text.text()) in data:
            # Передача данных о пользователе и открытие основного окна в случае успешного входа
            user = set(filter(lambda info: self.login_text.text() in info, select(["SELECT * from Users"])))
            login.close()
            yandex_mail.set_user(*user)
            yandex_mail.show()

        # Вывод ошибки в случае некорректных данных
        self.error_label.show() if (self.login_text.text(), self.password_text.text()) not in data\
            else self.error_label.hide()

    # Функция для перехода на окно регистрации
    def registration(self):
        login.close()
        registration.initUI()
        registration.show()

    # Функция отвечающая за видимость пароля
    def style_password(self):
        if self.password_hide:
            self.password_text.setEchoMode(QLineEdit.Normal)
            self.password_hide = False
        else:
            self.password_text.setEchoMode(QLineEdit.Password)
            self.password_hide = True


# Класс основного окна приложения
class Yandex_mail(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)

        # Объявляем необходимые переменные
        self.user = None
        self.user_info = []
        self.buttons = [self.incoming_message_button,
                        self.send_message_button,
                        self.spam_button,
                        self.new_message_button]
        self.id_messages = 1

    # Устанавливаем интерфейс
    def initUI(self):
        self.setWindowTitle('Yandex_lyceum')

        # Отображаем первоначально активную кнопку сообщений
        self.set_color_button(0, self.buttons)

        self.new_message_group.hide()
        self.send_button.hide()
        self.list_messages.show()
        self.read_message.hide()

        # Задаем стили заголовков
        self.welcome.setFont(QFont("Times", 10, QFont.Bold))
        self.title.setFont(QFont("Times", 12, QFont.Bold))
        self.user_name.setFont(QFont("Times", 8, QFont.Bold))
        self.user_name.setText(f'{self.user[1]} {self.user[2]}')

        # Первоначально отображаем на экран сообщений входящие письма из бд
        self.list_messages.clear()
        for message in set(filter(lambda user: self.user[0] in user and user[1],
                                  select(['SELECT recipient_login, topic, title, id from Messages']))):
            self.list_messages.addItem(f'|id:{message[3]}| {message[2]}')

        # Задаем стиль ошибкам при отправке нового сообщения
        self.user_error.setStyleSheet("color: red;")
        self.title_error.setStyleSheet("color: red;")
        self.message_error.setStyleSheet("color: red;")
        self.user_error.hide()
        self.title_error.hide()
        self.message_error.hide()

        # Обрабатываем нажатия на кнопки
        # self.send_button.clicked.connect(self.check_message)
        self.send_button.clicked.connect(self.send_new_message)

        self.exit_button.clicked.connect(self.func_exit)

        self.incoming_message_button.clicked.connect(self.incoming_message)

        self.send_message_button.clicked.connect(self.send_messages)

        self.spam_button.clicked.connect(self.spam)

        self.new_message_button.clicked.connect(self.new_message)

        self.list_messages.itemClicked.connect(self.open_message)

    # Функция принимающая всю информацию о вошедшем пользователе
    def set_user(self, user):
        self.user = user
        self.initUI()

    # Функция для отправки новых сообщений
    def send_new_message(self):
        self.user_error.show() if not self.list_users.currentText() else self.user_error.hide()
        self.title_error.show() if not self.title_message.text() else self.title_error.hide()
        self.message_error.show() if not self.message.toPlainText() else self.message_error.hide()
        # Отправляем всю информацию о сообщение в бд если все поля заполнены корректно
        if self.list_users.currentText() and self.title_message.text() and self.message.toPlainText():
            try:
                self.user_error.hide()
                recipient = list(filter(lambda info: self.list_users.currentText() in info, self.user_info))[0].split()[0]
                self.id_messages = len(select(['SELECT * FROM Messages'])) + 1
                insert([f"""INSERT INTO Messages VALUES
                        ('{self.id_messages}',
                         '{recipient}',
                         '{self.user[0]}',
                         '{self.title_message.text()}',
                         '{self.topic_message.text()}',
                         '{self.message.toPlainText()}')"""])

                # Очищаем все поля ввода для нового сообщения
                self.title_message.setText('')
                self.topic_message.setText('')
                self.message.setText('')
                self.list_users.setCurrentText('')
            except:
                self.user_error.show()

    # Функция выхода пользователя
    def func_exit(self):
        yandex_mail.close()
        login.initUI()
        login.show()

    # Функция отображающая входящих сообщений
    def incoming_message(self):
        self.new_message_group.hide()
        self.send_button.hide()
        self.list_messages.show()
        self.read_message.hide()

        self.set_color_button(0, self.buttons)

        self.list_messages.clear()
        for messange in set(filter(lambda user: self.user[0] in user and user[1],
                                   select(['SELECT recipient_login, topic, title, id from Messages order by id']))):
            self.list_messages.addItem(f'|id:{messange[3]}| {messange[2]}')

    # Функция отображающая все отправленные сообщения пользователем
    def send_messages(self):
        self.new_message_group.hide()
        self.send_button.hide()
        self.list_messages.show()
        self.read_message.hide()

        self.set_color_button(1, self.buttons)

        self.list_users.clear()
        self.list_users.addItem('')

        self.list_messages.clear()
        for message in set(filter(lambda user: self.user[0] in user and user[1],
                                  select(['SELECT sender_login, topic, title, id from Messages']))):
            self.list_messages.addItem(f'|id:{message[3]}| {message[2]}')

    # Функция отображающая сообщения попавшие в спам (без темы)
    def spam(self):
        self.new_message_group.hide()
        self.send_button.hide()
        self.list_messages.show()
        self.read_message.hide()

        self.set_color_button(2, self.buttons)

        self.list_messages.clear()
        
        for message in set(filter(lambda user: self.user[0] in user and not user[1],
                                  select(['SELECT recipient_login, topic, title, id from Messages']))):
            self.list_messages.addItem(f'|id:{message[3]}| {message[2]}')

    # Функция отображения интерфейса для отправки нового сообщения
    def new_message(self):
        self.new_message_group.show()
        self.list_messages.hide()
        self.send_button.show()
        self.read_message.hide()

        self.list_users.clear()
        self.list_users.addItem('')
        for user in set(item for item in select(["SELECT login, surname, name from Users"])):
            self.list_users.addItem(f'{user[0]} ({user[1]} {user[2]})')
            self.user_info.append(f'{user[0]} ({user[1]} {user[2]})')

        self.title_message.setText('')
        self.topic_message.setText('')
        self.message.setText('')

        self.set_color_button(3, self.buttons)

    # Функция для чтения выбранного сообщения
    def open_message(self):
        self.user_error.hide()
        sender = self.sender()
        id = int(sender.currentItem().text()[4:sender.currentItem().text().rfind('|')])
        self.list_messages.hide()
        self.read_message.show()

        message = list(filter(lambda letter: id in letter, select(['SELECT * from Messages'])))[0]
        sender = ' '.join(select([f'SELECT surname, name FROM Users WHERE login = "{message[2]}"'])[0])
        recipient = ' '.join(select([f'SELECT surname, name FROM Users WHERE login = "{message[1]}"'])[0])
        self.read_message.setText(f"От кого: \n{sender} \nПолучатель: \n{recipient}  \nНазвание: \n{message[3]} \nТема: \n{message[4]} \nСообщение: \n{message[5]}")

    # Функция для установки стилей нажатой и неактивных кнопок
    def set_color_button(self, index, buttons):
        for index_button, button in enumerate(buttons):
            if index == index_button:
                button.setStyleSheet("background-color: lightblue;")
            else:
                button.setStyleSheet("background-color: gray;")


# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Создание всех объектов классов
    login = Login()
    registration = Registration()
    yandex_mail = Yandex_mail()

    # Отображение стартового экрана входа
    login.show()

    # Завершение работы процесса при закрытие приложения
    sys.exit(app.exec())


# 1928374655#vlad#