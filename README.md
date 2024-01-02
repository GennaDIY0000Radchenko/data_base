В робочій директорії  
Перейти до робочої директорії :  
```cd C:\Users\админ\PycharmProjects\python_coding\_course_3\data_base\db_labs\lab3_test```  
де знаходяться ```.yml``` файли.  
```
lab3_test
 | app
 |  | requirements.txt
 |  | Dockerfile
 |  | data2019.csv
 |  | data2020.csv
 |  | main.py
 | flyway
 |  | sql
 |  |  | V2__ ... .sql
 |  |  | ...
 |  |  | V7__ ... .sql
 |  | flyway.conf
 | flask
 |  | static
 |  |  | styles.css
 |  | templates
 |  |  | filtres.html
 |  |  | main.html
 |  |  | tables.html
 |  | app.py
 |  | mongo_config.py
 |  | SQLA_config.py
 |  | Dockerfile
 |  | requirements.txt
 | datda_base.yml
 | app.yml
 | flyway.yml
 | redis.yml
 | flask.yml
 | README.md
```
Виконайте послідовно запити :  
Створення хостової машини:  
```docker-compose -f data_base.yml up --build --force-recreate -d```  
App:  
```docker-compose -f app.yml up --build --force-recreate -d```  
Flyway (зачекати закінчення роботи App) :  
```docker-compose -f flyway.yml up --build --force-recreate -d```  
Redis:  
```docker-compose -f redis.yml up --build --force-recreate -d```  
Flask:  
```docker-compose -f flask.yml up --build --force-recreate -d```  
```docker-compose -f mongo.yml up --build --force-recreate -d```   
  
Перевірити таблички  
```docker exec -it <copy num> psql -U postgres``` - для CMD  ```psql -U posrgres``` - для Terminal (data_base)  
```\c data_base;```  
```SELECT * FROM information_schema.tables WHERE table_schema LIKE 'public' AND table_type LIKE 'BASE TABLE';```  
  
Після завантаження даних (App):  
У файлі ```output.csv``` будуть зберігатися такі дані:  
Середній бал з Математики у кожному регіоні за 2019-2020 роки серед тих кому було зараховано тест  
У форматі:  
Назва регіону, середній бал за 2019 рік, середній бал за 2020 рік  
```...```, ```...```, ```...```  
А у файлі ```time.csv``` будуть зберігатися такі дані: 
Час (в секундаах), який було витрачено на завантаження даних у БД.  
У форматі:  
Час в секундах   
```...```  

Just in case :   
```docker system prune -a```
