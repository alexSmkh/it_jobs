import requests
from math import ceil
from main import get_average_salary


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
    return (jobs, total_jobs)


def get_programming_language_statistics_for_sj(job_list, total_jobs, language):
    vacancies_processed = 0
    total_salary = 0
    for job in job_list:
        average_salary = get_average_salary(job['payment_from'], job['payment_to'])

        if not average_salary:
            continue

        vacancies_processed += 1
        total_salary += average_salary

    programming_language_statistics = (
            language,
            total_jobs,
            vacancies_processed,
            int(total_salary/vacancies_processed)
    )
    return programming_language_statistics

