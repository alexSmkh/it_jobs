from terminaltables import DoubleTable


def get_probable_salary(minimum_value, maximum_value):
    if minimum_value and maximum_value:
        return (minimum_value + maximum_value) / 2
    elif minimum_value:
        return minimum_value * 1.2
    elif maximum_value:
        return maximum_value * 0.8


def get_statistics(language, count_vacancies, salaries):
    specified_salaries = [salary for salary in salaries if salary]
    vacancies_processed = len(specified_salaries)
    average_salary_for_language = int(max(specified_salaries)/vacancies_processed)

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
