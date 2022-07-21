# Сервис по поиску работы.
## Инструкция по установке и запуску проекта.
1. **Клонируйте репозитории с github.**

2. **Перейдите в директорию с проектом.**
```
cd job-service/
```
3. **Создайте виртуальное окружение.**
```
python3 -m venv venv
```
4. **Активируйте виртуальное окружение.**
```
source venv/bin/activate
```
5. **Установите зависимости.**
```
pip install -r requirements.txt
```
6. **Создайте файл конфигурации (например `env.sh`).**
```
touch env.sh
```
7. **Создайте БД PostgresSQL.**

8. **Заполните файл (`env.sh`) конфигурации.**
```
# SERVER ENV
export SERVER_HOST='localhost'
export SERVER_PORT=8000

# DATABASE ENV
export DB_HOST='localhost'
export DB_USER='fast'
export DB_PASSWORD='123QWE'
export DB_NAME='jobs' # название бд, которую вы создали

# JWT ENV
export JWT_SECRET_KEY='QWERRRR-WEQWQEW' # секретный ключ для jwt
export JWT_ALGORITHM='HS256' # алгоритм шифрования
```
9. **Активируйте файл конфигурации.**
```
source env.sh
```
10. **Выполните команду для работы с мигрвциями.**
```
export FLASK_APP=main.py
```
11. **Выполните комвнду для применения миграции.**
```
flask db upgrade
```
12. **Запустите приложение.**
```
python main.py
```




