from definitions_for_employees import *
from defenitions_for_clients import *
d = Definitions()
c = Defenitions_client()
while True:
    print('Добро пожаловать!!! Выберите действие : \n1 - авторизация\n2 - регистрация\nДля выхода любое другое число')
    e = input('Введите число ')

    if e == '1':
        #Авторизация...
        print('Выберите тип авторизации : \n1 - сотрудник\n2 - клиент\nЛюбое другое число - выход')
        i = input('Введите число ')
        if i == '1':
            # Вызывается функция для авторизации сотрудника
            id = d.employee_autor()
            if id == 0:
                continue
            else:
                # В случае успешной авторизации вызывается функция добавления товара или просмотра доступных заказов
                s = input('Введите 1 для просмотра доступных заказов\n0 для выхода\n2 для добавление количества товара\nЛюбое другое для добавление нового товара\n')
                if s == '1':
                    d.employee_choice(id)
                elif s == '0':
                    continue
                elif s == '2':
                    d.add_quanti(id)
                else:
                    d.add_good(id)

        if i == '2':
            #Вызывается функция для авторизации клиента
            id = c.client_autor()
            if id == 0:
                continue
            else:
                # В случае успешной авторизации вызывается функция для отправки заказа
                c.send_order(id)
    elif e == '2':
        #Вызывается функция для регистрации клиента
        c.client_registration()
    else:
        break



