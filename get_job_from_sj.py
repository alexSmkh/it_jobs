import requests
from dotenv import load_dotenv
from os import getenv
from math import ceil
from data_processing_functions import get_probable_salary


def fetch_jobs_from_sj(language):
    load_dotenv()
    url = 'https://api.superjob.ru/2.0/vacancies/'
    secret_key = getenv('KEY')
    params = {'count': 100, 'town': 'Москва'}
    headers = {'X-Api-App-Id': secret_key}

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
    probably_salaries = [
        get_probable_salary(job['payment_from'], job['payment_to'])
        for job in jobs
    ]
    return probably_salaries



