# Простейший чат на Tornado и Redis

Данный проект представляет собой простой чат с использованием `Tornado` в качестве веб-сервера и `Redis` для организации Pub/Sub механизма рассылки сообщений всем подключённым клиентам.

## Требования

- Python 3.x
- Redis (запущенный локально или доступный по сети)

Все необходимые модули Python указаны в файле `requirements.txt`.

## Установка зависимостей

Убедитесь, что у вас установлена утилита `pip`. Затем выполните в корневой директории проекта:

```bash
pip install -r requirements.txt
```
Данная команда установит все необходимые зависимости (включая tornado и redis).

## Запуск Redis
Если у вас ещё не запущен Redis-сервер, запустите его (предполагается, что Redis установлен локально).
Убедитесь, что Redis доступен по умолчанию на localhost:6379.

## Запуск приложения
Убедитесь, что вы находитесь в корневой папке проекта.

Запустите сервер Tornado командой:

```bash
py app.py
```
После успешного запуска вы увидите сообщения:

```
Connected to Redis successfully!
Redis listener started...
Server started at http://localhost:8888
```
Откройте веб-браузер и перейдите по адресу:

```
http://localhost:8888
```
Вы увидите простую страницу чата.

## Использование
В окне чата введите сообщение в текстовое поле и нажмите кнопку «Отправить».
Сообщение отправится на сервер, будет опубликовано в Redis.
Сервер, подписанный на канал Redis, получит сообщение и разошлёт его всем подключённым клиентам, включая отправителя.
Если открыть чат в нескольких вкладках или на нескольких устройствах, можно увидеть, что все они будут получать сообщения в реальном времени.
В левой части (или в зависимости от верстки — сверху) окна отображается список подключённых клиентов.

## Остановка
Для остановки сервера нажмите Ctrl+C в терминале, где был запущен сервер.

## Дополнительная информация
1. Файл server.py содержит основной код сервера Tornado, обработчик WebSocket, подключение к Redis и Pub/Sub логику.
2. Шаблон index.html, скрипт script.js и стили style.css находятся в соответствующих папках (templates, static) и обеспечивают клиентский интерфейс.
3. Файл requirements.txt содержит список всех необходимых библиотек Python для быстрого развёртывания проекта.