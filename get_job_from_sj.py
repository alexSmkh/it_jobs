import requests
from math import ceil
from data_processing_functions import get_average_salary


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


def get_salaries_from_sj(jobs):
    salaries = []
    for job in jobs:
        salaries.append(get_average_salary(
            job['payment_from'],
            job['payment_to'])
        )
    return salaries



