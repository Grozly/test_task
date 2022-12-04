# Тестовое задание (проект для РЖД)
### Задание:

Нужно реализовать сервис, который будет выступать в качестве моста между MQTT и telnet-клиентом, с которым можно будет общаться текстом.<br>

Клиентов может подключиться несколько (до 1000). С каждым из клиентов будет поддерживаться отдельная сессия.
Во время сессии клиент может подписаться на сообщения (командой `subscribe <topic>`) и начать слушать сообщения по подписке (командой `poll`).
Команды заканчиваются символом перевода строки. После ввода команды `poll` сервер должен начать выводить сообщения формата `{topic: value}`.
После команды `poll` сервер больше не реагирует на команды клиента (для упрощения).

### Пример сессии:
1.	Сервер запущен, подключился к брокеру `MQTT` и слушает входящие telnet-соединения на порту 1234.
2.	Подключился клиент 1, ввёл команду subscribe `topic1/foo`. Сервер подписался на сообщения для этих топиков, но входящие сообщения пока игнорирует (не было команды `poll`).
3.	Подключился клиент 2, ввёл команду subscribe `topic1/foo` и сразу за ней `poll`. Сервер подписался на этот топик и отправляет входящие сообщения в консоль второму клиенту.
4.	Клиент 1 ввёл команду `poll`. Сервер начинает отправлять входящие сообщения первому клиенту.

### Условия:
Можно использовать любые доступные библиотеки, лишь бы работало под ОС Linux.
С telnet-клиентом можно связываться через сырой TCP (сокеты).
Для `MQTT` рекомендуется использовать библиотеки `paho.mqtt`, доступны для `C`, `Python` и ещё множества языков.
В качестве брокера `MQTT` можно использовать mosquitto (доступен в Linux), для ручной записи в топики можно использовать утилиты `mosquitto_sub` и `mosquitto_pub`.


# Инструкция

### Запуск сервера:
1. Склонировать репозиторий.
2. В корне репозитория запустить `docker-compose up --build main`. `docker-compose` запустить сборку 2 контейнеров (приложение и брокер `mosquitto`)
3. Ждем пока приложение не отпишется, что сервер запущен, сообщение `Running Server on PORT 1234`
4. Ура! Наш сервер запущен, подключен к брокеру и слушает входящие соединения на порту `1234`.

### Проверка работы:
1. Запускаем терминал и подключаемся к серверу `telnet 127.0.0.1 1234`.
2. Мы должны увидеть приветсвенное сообщение `Please enter command [subscribe <some_topic>, poll]`..., если попробовать сразу вводить текст в сессии `telnet`, сервер никак на это не будет реагировать. Запускаем еще 2-3 клиента по `telnet`.
3. Пробуем проверить наш функционал. <br>
- Первый подключенный клиент подписывается на топик коммандой `subscribe topic1/foo` и сразу вводим комманду `poll` для прослушивания.<br>
- Второй подключенный клиент подписывается на топик `subscribe topic1/foo`, после попробуем отправить пару сообщений (123, 321).<br>
- Мы увидим, что первый клиент в консоль получил наши сообщения от сервера.<br>
- Второй клиент вводит команду `poll` и становится слушателем.<br>
- Третий клиент подписывается на топик `subscribe topic1/foo`, и отправляем сообщения ("hello", "goodbye").<br>

Первый и второй клиент получают эти сообщения от сервера. Done!

Все логи `mosquitto` можно посмотреть в режиме `real-time` по пути `log/mosquitto.log`.
Еще можно подключится к контейнеру `mosquitto` командой `docker-compose exec -it mosquitto sh`, далее можно подписаться на топик утилитой `mosquitto_sub` и мониторить все сообщения в топике.

