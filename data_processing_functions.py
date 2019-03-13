from terminaltables import DoubleTable


def get_average_salary(minimum_value, maximum_value):
    if minimum_value and maximum_value:
        return (minimum_value + maximum_value) / 2
    elif minimum_value:
        return minimum_value * 1.2
    elif maximum_value:
        return maximum_value * 0.8


def get_statistics(language, count_vacancies, salaries):
    vacancies_processed = 0
    total_salary = 0
    for salary in salaries:
        if not salary:
            continue
        vacancies_processed += 1
        total_salary += salary
    average_salary_for_language = int(total_salary/vacancies_processed)
    return (
        language,
        count_vacancies,
        vacancies_processed,
        average_salary_for_language
    )


def pretty_print(statistics, title):
    TABLE_DATA = (
        ('Язык программирования',
         'Вакансий найдено',
         'Вакансий отобрано',
         'Средняя з/п'),
        *statistics
    )
    table_instance = DoubleTable(TABLE_DATA, title)
    print(table_instance.table, end='\n\n\n')
