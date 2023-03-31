# test_etu
Простой Django-сервер, осуществляющий конвертацию данных, переданных в запросе, в необходимый xml-формат и наоборот

Описание процесса конвертации JSON -> XML: 

1) Получение JSON из тела запроса
2) Преобразование JSON в формат словаря (В случае, если поступает байтовая строка, то необходимо декодировать ее в формат utf-8) 
3) Преобразование в XML 

Описание процесса конвертации XML -> JSON: 
1) Получение XML из тела запрсоа
2) Декодирование в utf-8
3) Преобразование в формат словаря
4) Конвертация словаря в JSON


Проблемы с валидацией XML:
- При конвертации необходимо укзать корневой тег. Среда не видит корневой тег xs:scheme, однако пространство имен явно указано. 

Решение: не найдено

