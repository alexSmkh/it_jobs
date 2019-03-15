import requests
from data_processing_functions import get_probable_salary
from itertools import chain


def fetch_jobs_from_hh(url, params, language):
    params_copy = params.copy()
    params_copy['text'] = language
    params_copy['page'] = 0
    first_page_response = requests.get(url, params=params_copy).json()
    pages = first_page_response['pages']
    total_jobs = first_page_response['found']
    job_list = []
    while params_copy['page'] < pages:
        page = requests.get(url, params=params_copy).json()
        job_list.append(page['items'])
        params_copy['page'] += 1
    pretty_job_list = chain.from_iterable(job_list)
    return (pretty_job_list, total_jobs)


def get_salaries_from_hh(jobs):
    probable_salaries = [
        get_probable_salary(job['salary']['from'], job['salary']['to'])
        for job in jobs if job['salary']
    ]
    return probable_salaries
