import requests
from dotenv import load_dotenv
from os import getenv
from math import ceil
from terminaltables import DoubleTable


def fetch_jobs_from_hh(url, params, language):
    params_copy = params.copy()
    params_copy['text'] = language
    params_copy['page'] = 0
    first_page_response = requests.get(url, params=params_copy).json()
    pages = first_page_response['pages']
    job_page_list = []
    while params_copy['page'] < pages:
        job_page_list.append(requests.get(url, params=params_copy).json())
        params_copy['page'] += 1
    return (job_page_list, language)


def fetch_jobs_from_sj(url, headers, params, language):
    jobs = []
    params_copy = params.copy()
    params_copy['keyword'] = language
    response = requests.get(url, headers=headers, params=params_copy).json()
    total_jobs = response['total']
    page_count = ceil(total_jobs / 100)
    jobs.extend(response['objects'])
    if page_count > 0:
        for page in range(1, page_count):
            params_copy['page'] = page
            response = requests.get(url, headers=headers, params=params_copy).json()
            jobs.extend(response['objects'])
    return (language, jobs, total_jobs)


def get_programming_language_statistics_for_sj(language, job_list, total_jobs):
    vacancies_processed = 0
    total_salary = 0
    for job in job_list:
        salary = get_predict_rub_salary_sj(job['payment_from'], job['payment_to'])
        if not salary:
            continue
        vacancies_processed += 1
        total_salary += salary

    programming_language_statistics = (
            language,
            total_jobs,
            vacancies_processed,
            int(total_salary/vacancies_processed)
    )
    return programming_language_statistics


def get_programming_language_statistics_for_hh(job_page_list, language):
    vacancies_processed = 0
    total_salary = 0
    for job_page in job_page_list:
        jobs = job_page['items']
        for job in jobs:
            salary = job['salary']
            if not salary:
                continue

            if not get_predict_rub_salary_sj(salary['from'], salary['to']):
                continue
                
            vacancies_processed += 1
            total_salary += get_predict_rub_salary_sj(salary['from'], salary['to'])

    programming_language_statistics = (
        language,
        job_page['found'],
        vacancies_processed,
        int(total_salary/vacancies_processed)
    )
    return programming_language_statistics


def get_predict_rub_salary_sj(payment_from, payment_to):
    salary_from = payment_from
    salary_to = payment_to

    if salary_from is None:
        salary_from = 0
    if salary_to is None:
        salary_to = 0

    if salary_from != 0 or salary_to != 0:
        if salary_from != 0 and salary_to != 0:
            return (salary_from + salary_to)/2
        elif salary_from != 0:
            return salary_from * 1.2
        else:
            return salary_to * 0.8
    return None


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


if __name__ == '__main__':
    load_dotenv()
    url_for_hh = 'https://api.hh.ru/vacancies'
    url_for_sj = 'https://api.superjob.ru/2.0/vacancies/'
    area_code_moscow_for_hh = 1
    secret_key = getenv('KEY')

    params_for_hh = {'area': area_code_moscow_for_hh,'currency': 'RUR'}

    params_for_sj = {'count': 100, 'town': 'Москва'}
    header_for_sj = {'X-Api-App-Id': secret_key}

    top_programming_languages = [
        'JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'Go',
        'Ruby', 'Scala']

    statistics_from_sj = []
    statistics_from_hh = []
    for lang in top_programming_languages:
        statistics_from_sj.append(
            get_programming_language_statistics_for_sj(
                *fetch_jobs_from_sj(
                    url_for_sj,
                    header_for_sj,
                    params_for_sj,
                    lang))
        )
        statistics_from_hh.append(
            get_programming_language_statistics_for_hh(
                *fetch_jobs_from_hh(url_for_hh, params_for_hh, lang)))

    pretty_print(statistics_from_sj, 'SuperJob')
    pretty_print(statistics_from_hh, 'HeadHunter')
