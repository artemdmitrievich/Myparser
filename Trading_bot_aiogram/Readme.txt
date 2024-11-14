#Для размещения на сервере python anywhere
1. Зайти нa сайт, перейти в files и создать папку для бота
2. В эту папку добавить все файлы и папки, затем в папки добавить файлы и вложенные папки и т.д.
3. Нажать Dashboard, затем Bash
4. Установить библиотеки python -m pip install something
5. Перейти в папку с ботом cd Bot_derictory
6. Запустить бота python "Название файла для запуска бота".py


#Чтобы исправить ошибку ClientConnectorError: Cannot connect to host api.telegram.org:443 ssl:default [Network is unreachable]
1. Для начала нужно импортировать установить модуль aiohttp-socks в bash-консоли
pip install aiohttp-socks
2. Затем нужно импортировать модуль AiohttpSession
from aiogram.client.session.aiohttp import AiohttpSession
3. Теперь нужно создать переменную session
session = AiohttpSession(proxy='http://proxy.server:3128') # в proxy указан прокси сервер pythonanywhere, он нужен для подключения
4. В объекте бота указываем session=session
bot = Bot(token='...', session=session)