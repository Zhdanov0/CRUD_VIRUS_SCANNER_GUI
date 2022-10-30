# **CRUD_VIRUS_SCANNER_GUI**
-	Реализованы **основные функции для работы с базой данных**: создание таблицы, ее вывод, добавление, редактирование, удаление строк таблицы;

-	Реализован **графический интерфейс**;

-	Реализован **поиск "вирусных" файлов**;

# **СОЗДАНИЕ ТАБЛИЦЫ, ПОДГОТОВЛЕННЫЕ  ЗАПРОСЫ, МЕНЮ**
В качестве СУБД выбран PostgreSQL.

Сначала **создается таблица**, если такая не существует.  
```
cur.execute('''CREATE TABLE IF NOT EXISTS viruses (
                extension VARCHAR(50) NOT NULL,
                line VARCHAR(50) NOT NULL);''')
```

Далее создаются **подготовленные запросы** с целью увеличения производительности и сокращения кода.
```
cur.execute('''CREATE TABLE IF NOT EXISTS viruses (
                extension VARCHAR(50) NOT NULL,
                line VARCHAR(50) NOT NULL);''')

cur.execute('''PREPARE select_all_order AS
               SELECT * FROM viruses ORDER BY extension;''')

cur.execute('''PREPARE select_all AS
               SELECT * FROM viruses;''')

cur.execute('''PREPARE select_all_where AS 
               SELECT extension, line FROM viruses WHERE extension = $1 AND line = $2;''')

cur.execute('''PREPARE insert AS 
               INSERT INTO viruses (extension, line) VALUES ($1, $2);''')

cur.execute('''PREPARE update AS 
               UPDATE viruses SET extension = $1, line = $2 WHERE extension = $3 AND line = $4;''')

cur.execute('''PREPARE delete AS
               DELETE FROM viruses WHERE extension = $1 and line = $2;''')
```               

После запуска программы отображается **меню**. Для работы с базой данных можно выбрать:  
"Add line", "Edit database", "Show database".

![image](https://user-images.githubusercontent.com/116901579/198886889-0f8e0033-368f-4eb4-9fee-aac83535ae85.png)

# ДОБАВЛЕНИЕ ЗАПИСЕЙ
Для этого нужно ввести расширение и "вирусную" строку файла.  
Для примера по умолчанию написано расширение txt.

![image](https://user-images.githubusercontent.com/116901579/198886965-9ef38d38-4289-43c0-9eb4-37ff6b0d577b.png)

После ввода корректных данных и подтверждения добавления (кнопка "Add") будет выведено сообщение о успешном добавлении строки.

![image](https://user-images.githubusercontent.com/116901579/198887073-f51a826b-096f-452f-bb5a-0fc9f168ffbb.png)

## ОШИБКИ

1. Пустое поле ввода  
2. Попытка добавления уже имеющихся в таблице данных

![image](https://user-images.githubusercontent.com/116901579/198887249-c49df72b-9939-4d25-be67-68a97f6a9377.png)
![image](https://user-images.githubusercontent.com/116901579/198887366-ab7ca8fc-f40c-4a7b-8f54-ee9bb5b7c3a2.png)

Для выхода используется кнопка Menu.

# РЕДАКТИРОВАНИЕ И УДАЛЕНИЕ ЗАПИСЕЙ
Снизу полностью выводится таблица: номер записи, расширение, "вирусная" строка.  
Сверху находится приглашение на ввод номера записи. И кнопки для редактирования и удаления записи.

![image](https://user-images.githubusercontent.com/116901579/198887417-73c9ae1c-493b-4f87-8b46-7b4ee6f61715.png)

## УДАЛЕНИЕ ЗАПИСИ
Например, хотим удалить запись с номером 4.  
Вводим номер и нажимаем кнопку "Delete".

![image](https://user-images.githubusercontent.com/116901579/198887448-49069a4c-d7b1-453c-81a9-6e0ee2bbe30a.png)
![image](https://user-images.githubusercontent.com/116901579/198887452-039d368e-4c9b-4131-957a-13c4a198e8d3.png)

## РЕДАКТИРОВАНИЕ ЗАПИСИ
Для редактирования нужно ввести номер записи и нажать кнопку "Edit".  
После этого отобразятся поля ввода (заполненные данными по указанному номеру) для редактирования выбранной записи.  
Редактируем и нажимаем "Accept". 

![image](https://user-images.githubusercontent.com/116901579/198887504-4742ef7b-a3b6-4b8e-99b0-7f51f522a0c7.png)
![image](https://user-images.githubusercontent.com/116901579/198887506-3f14e8e2-ecb7-48d0-80f6-5ddfa9e62caf.png)

## ОШИБКИ

1.	Ввод номера, не соответствующего числу записей в таблице.
2.	Нечисловой ввод.
3.	Пустое поле ввода при редактировании.

![image](https://user-images.githubusercontent.com/116901579/198887518-62ecd402-335c-4668-a714-0dc270878936.png)
![image](https://user-images.githubusercontent.com/116901579/198887519-c7df1179-4c88-4f90-a630-56006913cbdf.png)
![image](https://user-images.githubusercontent.com/116901579/198887642-5f8fc802-e794-44c4-9a1b-26210d36d941.png)

# ВЫВОД ТАБЛИЦЫ

![image](https://user-images.githubusercontent.com/116901579/198887691-60e349d1-31a0-42bf-a1d3-5173d91e1635.png)

# Сканирование
"Вирусным" считается файл определенного расширения, содержащий "вирусную" строку.  
Информация о расширениях и их "вирусных" строках хранится в таблице.  
Перед сканированием выполняется один запрос к базе данных и создается кэш. В качестве кэша используются префиксные деревья (модуль trie) для каждого расширения указанного в базе данных.  

![image](https://user-images.githubusercontent.com/116901579/198887751-d651f614-bfa1-4c8c-80f4-503225ca279a.png)

Необходимо ввести директорию для сканирования. Для вставки можно нажать "Paste".  
Начать сканирование – "Start".  
При сканировании проверяется каждый файл, найденный в директории и ее поддиректориях.  
Если расширение файла есть в таблице, то файл открывается и проверяется на наличие в нем "вирусной" строки.  
Для этого используется библиотека OS.  

## РЕЗУЛЬТАТ СКАНИРОВАНИЯ

![image](https://user-images.githubusercontent.com/116901579/198887794-f5c3f835-81fb-4e2a-aab1-1c80ecbcc89b.png)

Выводится:  
*	общее количество обработанных файлов; 
*	количество "вирусных" файлов;
*	количество ошибок анализа файлов (например, не хватает прав на чтение файла);
*	время выполнения сканирования;
*	информация о найденных "вирусных" файлах: название и путь.

После нажатия кнопки "Defuse" удаляются все "вирусные" файлы, результат сканирования обновляется.

![image](https://user-images.githubusercontent.com/116901579/198887856-8d1098af-1fda-4f28-af02-c271d27b222c.png)

## ОШИБКИ

* Ввод несуществующей директории

![image](https://user-images.githubusercontent.com/116901579/198887886-6c7d0df2-1772-44bc-9fb3-e50ebabdbc70.png)



