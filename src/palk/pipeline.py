import os

from utils import TIME_FORMAT_TIME_ID, Git, Time, TSVFile

from palk._common import DIR_REPO, GIT_REPO_URL, REPO_BRANCH_DATA, log
from palk.AppointmentPage import AppointmentPage
from palk.AvailabilityReport import AvailabilityReport
from palk.SummaryReport import SummaryReport

N_DAYS = 60
FORCE_SCRAPE = True

if __name__ == '__main__':
    all_timeslots = AppointmentPage.get_all_timeslots()
    data_list = [x.to_dict for x in all_timeslots]

    git = Git(GIT_REPO_URL)
    git.clone(DIR_REPO)
    git.checkout(REPO_BRANCH_DATA)

    if data_list:

        latest_file_name = os.path.join(DIR_REPO, 'palk.latest.tsv')
        TSVFile(latest_file_name).write(data_list)
        log.info(f'Wrote data to "{latest_file_name}".')

        time_now = Time()
        time_id = TIME_FORMAT_TIME_ID.stringify(time_now)
        history_file_name = f'/tmp/palk.{time_id}.tsv'
        latest_file_name = os.path.join(DIR_REPO, f'palk.{time_id}.tsv')
        TSVFile(history_file_name).write(data_list)
        log.info(f'Wrote data to "{history_file_name}".')

    availability_report = AvailabilityReport(all_timeslots)
    availability_report.save()

    summary_report = SummaryReport()
    summary_report.save()
