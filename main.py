from get_job_from_hh import fetch_jobs_from_hh
from get_job_from_hh import get_salaries_from_hh
from get_job_from_sj import get_salaries_from_sj
from get_job_from_sj import fetch_jobs_from_sj
from data_processing_functions import pretty_print
from data_processing_functions import get_statistics


def main():
    top_programming_languages = [
        'JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'Go',
        'Ruby', 'Scala']

    statistics_from_hh = []
    statistics_from_sj = []

    for lang in top_programming_languages:
        job_list_from_sj, count_of_jobs_sj = fetch_jobs_from_sj(lang)
        job_list_from_hh, count_of_jobs_hh = fetch_jobs_from_hh(lang)

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
