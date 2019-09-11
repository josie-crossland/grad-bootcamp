import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta

ADULT_PATIENT_AGE_THRESHOLD = 16


def get_csv_data(csv_file_name):
    with open(csv_file_name, "r") as f:
        csv_reader = csv.DictReader(f)
        data_rows = []
        for row in csv_reader:
            data_rows.append(row)

        return data_rows


def get_is_child_patient(date_of_birth):
    patient_age = relativedelta(datetime.now(), date_of_birth)
    return int(patient_age.years) < ADULT_PATIENT_AGE_THRESHOLD
