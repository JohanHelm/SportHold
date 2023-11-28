План график разработки сервиса

1й Этап

    Разработка и запуск Бота с расписанием для пользователей из группы Consumers.
    Объекты и параметры расписаний вносятся вручную. Дальше расписания генерятся для объектов.
    Consumers в боте создают слоты. Providers считывают информацию о занятых слотах на выбранный ими день.

    Срок исполнения 31.12.2023
    
2й Этап

    Разработка бота конструктора.
    
    Providers создают бота у Отца, затем вносят токен и имя бота в конструктор. Регистрируют свои объекты(rental) в конструкторе.
    Создают или выбирают расписание для обекта из наших типовых вариантов. Жмакуют на кнопку создать бота. Мы собираем параметры бота в текстовик и после нажатия кнопки "Создать бота" запускаем скрипт python start_bot.py -c params.txt.
    Для провайдров нужен пробный период, затем подписка. Необходимо придумать тарифы, цена пропорциональна кол-ву объектов. Необходимо прикрутить платёжку.
    Отслеживать срок действия подписки и кол-во бабла на счету провайдера. Оповещать об окончании подписки и при нулевом балансе останавливать ботов с расписаниями.
    
    Срок исполнения  31.03.2024
    
Пысы 1: После появления ощутимого количества ботов с расписаниями пишем бота каталог. 
Пысы 2: При возикновении необходимости управления хозяйством с мобильника пишем бота для админов, выносим в него какой-нибудь экстренный функционал.
Пысы 3: Паралельно с графиком разработки должен существовать и выполняться план-график продвижения сервиса на рынок, но я ни в одном глазу про этот проклятый маркетинг. 
    