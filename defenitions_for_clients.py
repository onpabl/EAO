import psycopg2


class Defenitions_client():

    def client_registration(self):
        #Регистрация клиентов
        connect = psycopg2.connect(database='eao', user='postgres', host='localhost', password='54-71394')
        cursor = connect.cursor()
        registr = False
        while registr == False:
            a = input('Введите 0 для выхода из регистрации\nЛюбое другое число для продолжения')
            if a == '0':
                return
            else:
                name = input('Добро пожаловать! Введите ваше имя : ')
                try:
                    password = int(input('Введите пароль. Пароль должен состоять исключительно из цифр : '))
                except Exception:
                    print('Неверный формат пароля!')
                    continue
                try:
                    number = int(input('Введите номер телефона. Он должен состоять исключительно из цифр : '))
                except Exception:
                    print('Неверный формат номера!')
                    continue
                try:
                    cursor.execute('insert into clients '
                                   'values(default, ' + str(password) + ', ' + str(number) + ', \'' + name + '\');')
                    connect.commit()
                    cursor.execute(
                        'select id, pass from clients where id = (select max(id) from clients);')
                    person_id = cursor.fetchall()
                    print('Ваш id для входа = ' + str(person_id[0][0]) + '\nВаш пароль = ' + str(person_id[0][1]))
                    registr = True
                except psycopg2.IntegrityError:
                    print('Пользователь с таким номером уже существует!!!')
        connect.close()


    def client_autor(self):
        #Авторизация клиента
        connect = psycopg2.connect(database='eao', user='postgres', host='localhost', password='54-71394')
        cursor = connect.cursor()
        while True:
            try:
                id = int(input('Введите ваш id '))
                password = int(input('Введите ваш пароль'))
                break
            except Exception:
                print('Неверный формат ввода')
        sql = "select pass from clients" \
              " where pass = " + str(password) + ' and id = ' + str(id) + ';'
        cursor.execute(sql)
        if len(cursor.fetchall()) == 0:
            print('Ошибка входа. Неверное id или пароль')
            return 0
        else:
            print('Вход выполнен')
            return id
        connect.close()

    def send_order(self, client_id):
        #Каталог доступных товаров + заказ. Вывод товаров по отделам
        connect = psycopg2.connect(database='eao', user='postgres', host='localhost', password='54-71394')
        cursor = connect.cursor()
        while True:
            cursor.execute('select * from goods where d_id = 4;')
            goods = cursor.fetchall()
            g_count = 0
            print('_____Пицца_____')
            for i in goods:
                g_count += 1
                print('Товар под номером ' + str(i[0]) + ' |  ' + i[4] + ' | Цена : ' + str(
                    i[2]) + ' | Количество : ' + str(i[3]))
            print('_____Суши_____')
            cursor.execute('select * from goods where d_id = 5;')
            goods = cursor.fetchall()
            for i in goods:
                g_count += 1
                print('Товар под номером ' + str(i[0]) + ' |  ' + i[5] + ' | Цена : ' + str(
                    i[2]) + ' | Количество : ' + str(i[3]))
            print('_____Десерт_____')
            cursor.execute('select * from goods where d_id = 6;')
            goods = cursor.fetchall()
            for i in goods:
                g_count += 1
                print('Товар под номером ' + str(i[0]) + ' |  ' + i[5] + ' | Цена : ' + str(
                    i[2]) + ' | Количество : ' + str(i[3]))
            print('__________')
            if g_count == 0:
                print('Упс, товаров нет(((')
                return
            i = input('Введите 0 для выхода\n1 - для просмотра описания товара\nЛюбое другое число для оформления заказа ')
            if i == '0':
                return
            # Заказ
            elif i == '1':
                while True:
                    try:
                        num = int(input('Введите номер товара, что бы узнать описание'))
                        break
                    except ValueError:
                        print('Введите число!!!')
                cursor.execute('select about from goods '
                               'where id = ' + str(num) +';')
                about = cursor.fetchall()
                if len(about) > 0:
                    print(about[0][0])
                else:
                    print('Не существует такого товара!!!')
            else:
                while True:
                    try:
                        g_id = int(input('Введите номер товара '))
                        quanti = int(input('Введите количество '))
                        break
                    except Exception:
                        print('Неккоректный ввод!')
                        continue
                cursor.execute('select count,price from goods where id = ' + str(g_id) + ';')
                available = cursor.fetchall()
                if len(available) == 0:
                    print('Такого товара нет!')
                    continue
                if quanti <= available[0][0]:
                    #Проверка на наличие нужного количества
                    cost = quanti * available[0][1]
                    print('Стоимость заказа будет составлять ' + str(cost))
                    while True:
                        try:
                            a = int(input('Введите 0 для отмены заказа\nЛюбое друго число для подтверждения заказа'))
                            break
                        except Exception:
                            print('Неккоректный ввод!')
                    if a == 0:
                        continue
                    cursor.execute('insert into orders '
                                   'values(default, ' + str(client_id) + ', ' + str(g_id) + ', ' + str(quanti) + ', ' + str(cost) + ', 0);')
                    cursor.execute('update goods set count = count - ' + str(quanti) + ' where id = ' + str(g_id) +';')
                    connect.commit()
                    print('Заказ успешно оформлен!')
                else:
                    print('Нет столько товара(((')
        connect.close()