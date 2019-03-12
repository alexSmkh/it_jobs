import requests
from data_processing_functions import get_average_salary


def fetch_jobs_from_hh(url, params, language):
    params_copy = params.copy()
    params_copy['text'] = language
    params_copy['page'] = 0
    first_page_response = requests.get(url, params=params_copy).json()
    pages = first_page_response['pages']
    total_jobs = first_page_response['found']
    job_page_list = []
    while params_copy['page'] < pages:
        job_page_list.append(requests.get(url, params=params_copy).json())
        params_copy['page'] += 1
    return (job_page_list, total_jobs)


def get_salaries_from_hh(job_pages):
    salaries = []
    for job_page in job_pages:
        jobs = job_page['items']
        for job in jobs:
            salary = job['salary']
            if not salary:
                continue
            if not get_average_salary(salary['from'], salary['to']):
                continue
            salaries.append(get_average_salary(salary['from'], salary['to']))
    return salaries
