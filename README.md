# Сравниваем вакансии программистов 
* Скрипт собирает и выводит в консоль статистику по з/п программистов среди
 самых популярных языков программирования.
* Статистика собирается по г. Москва с сайтов [HeadHunter](https://hh.ru/)
 и [SuperJob](https://www.superjob.ru/).
### Как установить 
* Должен быть установлен `python3`. Затем используйте `pip`(или `pip3`, 
 если есть конфликт с `Python2`) для установки зависимостей: 
 ```bash
 pip install -r requirements.txt
 ```
 * Для изоляции проекта рекомендуется использовать 
 [virtualenv/venv](https://docs.python.org/3/library/venv.html)
 * Чтобы получить доступ к API SuperJob, нужно создать файл `.env` и записать
 в него Ваш ключ:
 ```txt
 KEY='ваш_ключ'
  ```
* Ключ(X-Api-App-Id) Вы получите, как только зарегистрируете свое приложение
 в [личном кабинете](https://api.superjob.ru/#gettin):
* Файл `.env` необходимо положить в одну директорию со скриптом.

### Как запустить
```bash
python3 main.py
```
 
 ### Цель проекта
 Код написать в образовательных целях на онлайн-курсе для веб-разработчиков 
 [dvmn.org](dvmn.org)