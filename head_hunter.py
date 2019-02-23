import requests
from json import dumps


def get_all_jobs(url, params, language):
    params['text'] = language
    params['page'] = 0
    first_page_response = requests.get(url, params=params).json()
    pages = first_page_response['pages']
    job_page_list = []
    while params['page'] < pages:
        job_page_list.append(requests.get(url, params=params).json())
        params['page'] += 1
    return job_page_list


def get_programming_language_statistics(job_page_list):
    vacancies_processed = 0
    total_salary = 0
    for job_page in job_page_list:
        jobs = job_page['items']
        for job in jobs:
            if predict_rub_salary(job['salary']):
                vacancies_processed += 1
                total_salary += predict_rub_salary(job['salary'])

    programming_language_statistics = {
        'vacancies_found': job_page['found'],
        'vacancies_processed': vacancies_processed,
        'average_salary': int(total_salary/vacancies_processed)
    }
    return programming_language_statistics


def predict_rub_salary(salary_info):
    if salary_info:
        if salary_info['from'] and salary_info['to']:
            return (salary_info['from'] + salary_info['to'])/2
        elif salary_info['from']:
            return salary_info['from'] * 1.2
        else:
            return salary_info['to'] * 0.8
    return None


def print_statistics(statistics):
    pretty_json = dumps(statistics, indent=4, sort_keys=True)
    print(pretty_json)


if __name__ == '__main__':
    url_for_request = 'https://api.hh.ru/vacancies'
    area_code_for_moscow = 1
    top_programming_languages = [
        'JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'Go',
        'Ruby', 'Scala']
    params = {
        'area': area_code_for_moscow,
        'currency': 'RUR'}

    programming_languages_statistics = {
        programming_language: get_programming_language_statistics(
            get_all_jobs(url_for_request, params, programming_language)
        ) for programming_language in top_programming_languages}

    print_statistics(programming_languages_statistics)

