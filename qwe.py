import psycopg2
connect = psycopg2.connect(database='eao', user='postgres', host='localhost', password='54-71394')
cursor = connect.cursor()
name = input('name ')
about = input('about ')
cursor.execute('insert into goods values(default, 4, 250.36 , 25 ,\'' + name + '\', ' + '\'' + about + '\');')