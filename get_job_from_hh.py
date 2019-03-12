import requests
from tools import get_average_salary


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
    return job_page_list


def get_programming_language_statistics_for_hh(job_page_list, language):
    vacancies_processed = 0
    total_salary = 0
    for job_page in job_page_list:
        jobs = job_page['items']
        for job in jobs:
            salary = job['salary']
            if not salary:
                continue

            if not get_average_salary(salary['from'], salary['to']):
                continue

            vacancies_processed += 1
            total_salary += get_average_salary(salary['from'], salary['to'])

    programming_language_statistics = (
        language,
        job_page['found'],
        vacancies_processed,
        int(total_salary/vacancies_processed)
    )
    return programming_language_statistics