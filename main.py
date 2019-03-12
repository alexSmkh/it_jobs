from dotenv import load_dotenv
from os import getenv
from get_job_from_hh import *
from get_job_from_sj import *
from data_processing_functions import pretty_print
from data_processing_functions import get_statistics


def main():
    load_dotenv()
    url_for_hh = 'https://api.hh.ru/vacancies'
    url_for_sj = 'https://api.superjob.ru/2.0/vacancies/'
    area_code_moscow_for_hh = 1
    secret_key = getenv('KEY')

    params_for_hh = {'area': area_code_moscow_for_hh, 'currency': 'RUR'}

    params_for_sj = {'count': 100, 'town': 'Москва'}
    header_for_sj = {'X-Api-App-Id': secret_key}

    top_programming_languages = [
        'JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'Go',
        'Ruby', 'Scala']

    statistics_from_hh = []
    statistics_from_sj = []

    for lang in top_programming_languages:
        job_list_from_sj, count_of_jobs_sj = fetch_jobs_from_sj(
            url_for_sj,
            header_for_sj,
            params_for_sj,
            lang)

        job_list_from_hh, count_of_jobs_hh = fetch_jobs_from_hh(
            url_for_hh,
            params_for_hh,
            lang)

        salaries_from_hh = get_salaries_from_hh(job_list_from_hh)
        salaries_from_sj = get_salaries_from_sj(job_list_from_sj)

        statistics_from_sj.append(get_statistics(
            lang,
            count_of_jobs_sj,
            salaries_from_sj)
        )
        statistics_from_hh.append(
            get_statistics(lang, count_of_jobs_hh, salaries_from_hh)
        )

    pretty_print(statistics_from_sj, 'SuperJob')
    pretty_print(statistics_from_hh, 'HeadHunter')


if __name__ == '__main__':
    main()
