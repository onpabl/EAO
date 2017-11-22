import psycopg2


class Definitions():

    def employee_autor(self):
        # Авторизация пользователя
        connect = psycopg2.connect(database='eao', user='postgres', host='localhost', password='54-71394')
        cursor = connect.cursor()
        while True:
            try:
                id = int(input('Введите ваш id '))
                password = int(input('Введите ваш пароль'))
                break
            except Exception:
                print('Неверный формат ввода')
        sql = "select pass from departments" \
              " where pass = " + str(password) + ' and id = ' + str(id) + ';'
        cursor.execute(sql)
        if len(cursor.fetchall()) == 0:
            print('Ошибка входа. Неверное id или пароль')
            return 0
        else:
            print('Вход выполнен')
            return id

    def employee_choice(self, id):
        #Работа с заказами
        connect = psycopg2.connect(database='eao', user='postgres', host='localhost', password='54-71394')
        cursor = connect.cursor()
        while True:
            cursor.execute('select * from orders '
                           'where (select d_id from goods '
                           'where id = orders.g_id) = ' + str(id) + ' and status = 0;')
            results = cursor.fetchall()
            if len(results) == 0:
                print('Доступных заказов нет!')
                break
            for i in results:
                cursor.execute('select name from goods where id = ' + str(i[2]) + ';')
                good = cursor.fetchall()
                print('Номер заказа : ' + str(i[0]) + '\n Имя товара : ' + good[0][0] + '\n Количество : ' + str(i[3]))

            while True:
                try:
                    a = int(input('Введите выбранный номер заказа или 0 для выхода : '))
                    break
                except ValueError:
                    print('Неверный формат ввода, введите число!')
            if a == 0:
                break
            change = -1
            confirm = -1
            for i in results:
                if i[0] == a:
                    print('___Подтверждение выбора заказа___')
                    print('Номер заказа : ' + str(i[0]) + '\n Имя товара : ' + good[0][0] + '\n Количество : ' + str(i[3]))
                    while confirm != '0' and confirm != '1':
                        confirm = input('Введите 0 для отмены\n1 для подтверждения')
                    if confirm == '0':
                        change = 0
                        continue
                    else:
                        cursor.execute('update orders set status = 1 where id = ' + str(a) + ';')
                        connect.commit()
                        change = 1
            if change == 1:
                print('Заказ принят успешно')
            elif change == -1:
                print('Ошибка принятия заказа. Неверно введен номер заказа!!!')
            else:
                print('Выбор заказа отменен')
        connect.close()


    def add_good(self, id):
        #Добавление нового товара
        connect = psycopg2.connect(database='eao', user='postgres', host='localhost', password='54-71394')
        cursor = connect.cursor()
        name = input('Введите название товара : ')
        about = input('Введите описание товара : ')
        while True:
            try:
                cost = int(input('Введите цену товара : '))
                quanti = int(input('Введите количество : '))
                break
            except:
                print('Неверный формат ввода, введите числа!')
        print('Имя товара : ' + name + '\nОписание : ' + about + '\nЦена : ' + str(cost) + '\nКоличество : ' + str(quanti))
        a = input('Введите 0 для отмены\nЛюбое другое число для подвтерждения')
        if a == '0':
            return
        else:
            cursor.execute('insert into goods '
                           'values(default, ' + str(id) + ', ' + '\'' + name + '\', ' + '\'' + about + '\', ' + str(cost) + ', ' + str(quanti) + ';')
            connect.commit()
        connect.close()

    def add_quanti(self, id):
        #Добавление количества товара
        connect = psycopg2.connect(database='eao', user='postgres', host='localhost', password='54-71394')
        cursor = connect.cursor()
        cursor.execute('select * from goods '
                       'where d_id = ' + str(id) + ';')
        goods = cursor.fetchall()
        for i in goods:
            print('Товар под номером ' + str(i[0]) + ' |  ' + i[5] + ' | Количество : ' + str(i[3]))
        ex = input('0 для отмены\nЛюбое другое число для продолжения\n')
        if ex == '0':
            return
        while True:
            try:
                good_num = int(input('Введите номер товара'))
                add = int(input('Введите количества товара, которое нужно добавить'))
                break
            except ValueError:
                print('Введите число!')
        cursor.execute('update goods set count = count + ' + str(add) + ' where id = ' + str(good_num) + ';')
        connect.commit()
        print('Теперь товара больше!')
        connect.close()