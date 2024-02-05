![](https://telegra.ph/file/1e82726556d321d84e2b6.png)
# Установка контейнера easyXray (3X-UI + Traefik + Telegram Bot)
Инструкция будет включать в себя:

1.  Установка контейнера easyXray (3X-UI + Traefik + Telegram Bot)
2.  Настройка

Для установки понадобится:

1.  **VPS или иной сервер с доступом к консоли SSH**
2.  **1 ГБ ОЗУ**
3.  **Debian не ниже версии 9 или Ubuntu не ниже 20.04 (инструкция может работать и на других дистрибутивах, но некоторые детали будут отличатся)**

Официальный репозиторий 3X-UI: [https://github.com/MHSanaei/3x-ui](https://github.com/MHSanaei/3x-ui)

Официальный репозиторий форка X-UI: [https://github.com/alireza0/x-ui](https://github.com/alireza0/x-ui)

[Traefik](https://github.com/traefik/traefik) (используется для выпуска сертификатов и проксирования через HTTPS админской панели 3X-UI) 

Скачиваем скрипт, делаем файл исполняемым и запускаем установку:

    curl -sSL https://raw.githubusercontent.com/Team418-git/easyXray/main/setup.sh -o setup.sh && chmod +x setup.sh && ./setup.sh

Скрипт проверит наличие установленного Docker и спросит разрешение на установку из официального репозитория Docker если он ещё не установлен и далее запросит:

Имя пользователя для панели администратора - **"Enter username for 3X-UI Panel"**

Пароль администратора - **"Enter password"**

Порт подключения к панели администратора - **"Enter port on which 3X-UI would be available: "**

имя хоста (домен) или IP если домен отсутствует **"Enter your hostname:"**

Ваш адрес почты для сертификата **"Enter your e-mail for certificate:"**

API токен вашего телеграм бота (подробнее [тут](https://medium.com/geekculture/generate-telegram-token-for-bot-api-d26faf9bf064)) **"Enter your Telegram bot API token:"**

Имя пользователя Telegram администратора без @ (не ID) - **"Enter your Telegram admin profile"**

Также сервер спросит хотите ли вы заменить таблицу inbounds (она содержит данные о клиентах и конфигурациях прокси, по умолчанию пустая) - первый запуск скрипта заменяет пустую таблицу, последующий запуск заменит данные на дефолтную конфигурацию с Vless XTLS-Reality, порт 443.

По завершении работы скрипт выдаст адрес подключения к панели администратора.

3X-UI, Traefik и Telegram бот установлены и работают.     

**Видео с установкой easyXray:** (кликабельно)        
[![Видео установки](https://telegra.ph/file/2383c7ea0db55ab8a376e.jpg)](https://youtu.be/fjtPnENbYKU)     

Для настройки через Веб UI:

Для 3X-UI переходим по адресу _https://yourIPorDomain:PORT,_ где yourIPorDomain - IP-адрес вашего сервера или доменное имя, если оно у вас есть и настроено

Для настройки через Telegram Бота:
От администратора:
1. Перейдите в вашего бота Telegram
2. Запустите команду /start

![](https://telegra.ph/file/fb92abe35cc048814a85e.jpg)   
3. **Для добавления пользователя:**   
  3.1 Добавить юзера   

![](https://telegra.ph/file/75c44676a24a1b0a5d59e.jpg)   

  3.2 Ввести имя пользователя (без @)   
  3.3 Ввести количество (лимит) уникальных конфигураций (равно количеству устройств) которые пользователь может получить    
4. **Для получения ссылки-конфигурации:**     
   От ранее добавленного пользователя (п.3) или Администратора (username администратора так же необходимо добавить через п.3)   
  4.1 Нажать кнопку "Запросить конфигурацию"     
  Каждый пользователь может запросить столько конфигураций, сколько указано в пункте 3    

![](https://telegra.ph/file/bf9bd70ec7cf2929d5ddf.jpg)

5. **Для удаления пользователя:**   
5.1 Кнопка "Удалить юзера"     
5.2 Ввести имя пользователя (без @)     
![](https://telegra.ph/file/c5360e9ea4376b7cb5707.jpg)     

Так же бот содержит ссылки на инструкции по подключению устройств на платформах: MacOS, Windows, Linux, iOS, Android для клиентов [FoxRay](https://apps.apple.com/us/app/foxray/id6448898396) и [Hiddify Next](https://github.com/hiddify/hiddify-next)

Для настройки клиентов через админскую панель:
![](https://telegra.ph/file/7eb8f8013da91cfbfebe0.png)      
 Выбираем Меню   
![](https://telegra.ph/file/d085c978b3c622d54a875.png)      
Добавить пользователя   
![](https://telegra.ph/file/d2721d1ed8a72f8398b45.png)      
Меняем необходимые данные или оставляем по умолчанию (ID должен соответствовать формату UUID)   
![](https://telegra.ph/file/12f1372bb3b3239746968.png)     
Ограничение по IP - количество одновременно подключенных устройств по данному пользователю   
Flow - xtls-rprx-vision    
Общий расход - ограничение расхода (при превышении необходимо будет сбросить счетчик трафика)    
Срок действия конфигурации (Дата окончания) - дата истечения конфигурации (будет деактивирована, но не удалена)    
![](https://telegra.ph/file/e97259146bedf9ce7394c.png)      
  по значку QR - отобразить QR Код для подключения, который можно отсканировать камерой в мобильных клиентах ([v2rayNG](https://github.com/2dust/v2rayNG/releases) или [Nekobox](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases) на Android, [Wings X](https://apps.apple.com/us/app/wings-x/id6446119727)/[FoXray](https://apps.apple.com/us/app/foxray/id6448898396) или [Shadowrocket](https://apps.apple.com/us/app/shadowrocket/id932747118) на iOS)
![](https://telegra.ph/file/9120e5869e7e5dd352357.png)      
по значку I (info) - информация о подключении и ссылка на конфиг (vless://)    

Также по кнопке "Меню" можно сбросить счетчики трафика, добавить пользователей (в том числе сгенерировать разом N аккаунтов по шаблону).    
