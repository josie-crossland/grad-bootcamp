from datetime import datetime
from utils import get_is_child_patient

MAXIMUM_DAYS_TO_WAIT_FOR_TREATMENT_START_ADULT = 60
MAXIMUM_DAYS_TO_WAIT_FOR_TREATMENT_START_CHILD = 30


def validate_records(data):
    record_is_valid = False
    for record in data:
        error_messages = []
        patient_id = record.get('patient_id', None)
        try:
            date_format = "%d/%m/%Y"
            date_of_birth = datetime.strptime(record['date_of_birth'], date_format)
            date_first_seen = datetime.strptime(record['date_first_seen'], date_format)
            date_of_diagnosis = datetime.strptime(record['date_of_diagnosis'], date_format)
            treatment_start_date = datetime.strptime(record['treatment_start_date'], date_format)
            treatment_end_date = datetime.strptime(record['treatment_end_date'], date_format)
            cancer_type = int(record['cancer_type'])
            treatment_type = int(record['treatment_type'])

            is_child_patient = get_is_child_patient(date_first_seen, date_of_birth)

            is_valid_date_sequence = validate_date_sequence(date_first_seen, date_of_diagnosis,
                                                            treatment_start_date, treatment_end_date)

            is_valid_treatment_delay = validate_treatment_delay(date_of_diagnosis, treatment_start_date,
                                                                is_child_patient)

            is_valid_treatment_type = validate_treatment_type(cancer_type, treatment_type)

            if is_valid_date_sequence and is_valid_treatment_delay and is_valid_treatment_type:
                record_is_valid = True
                message = f'Success - valid record - patient {patient_id}'
                print(record_is_valid, message)

            if not is_valid_date_sequence:
                record_is_valid = False
                error_messages.append(f'Failure - invalid date sequence - patient {patient_id}')

            if not is_valid_treatment_delay and is_child_patient:
                record_is_valid = False
                error_messages.append(f'Failure - more than thirty days between diagnosis and treatment start'
                                      f' - patient {patient_id}')
            elif not is_valid_treatment_delay and not is_child_patient:
                record_is_valid = False
                error_messages.append(f'Failure - more than sixty days between diagnosis and treatment start'
                                      f' - patient {patient_id}')

            if not is_valid_treatment_type:
                record_is_valid = False
                error_messages.append(
                    f'Failure - invalid treatment type {treatment_type} for cancer type {cancer_type} '
                    f'- patient {patient_id}')

            if error_messages:
                print(record_is_valid, error_messages)

        except ValueError as e:
            record_is_valid = False
            error_messages.append(f'Failure - {e} - patient {patient_id}')
            print(record_is_valid, error_messages)


def validate_date_sequence(first_seen, diagnosis, treatment_start, treatment_end):
    return first_seen < diagnosis < treatment_start < treatment_end


def validate_treatment_delay(diagnosis, treatment_start, is_child):
    time_waited_for_treatment = treatment_start - diagnosis
    if is_child:
        return time_waited_for_treatment.days <= MAXIMUM_DAYS_TO_WAIT_FOR_TREATMENT_START_CHILD
    else:
        return time_waited_for_treatment.days <= MAXIMUM_DAYS_TO_WAIT_FOR_TREATMENT_START_ADULT


def validate_treatment_type(cancer_type, treatment_type):
    cancer_type_3_treatments = [3, 4, 5]
    cancer_type_4_treatments = [1, 2]
    if cancer_type == 3:
        return treatment_type in cancer_type_3_treatments
    elif cancer_type == 4:
        return treatment_type in cancer_type_4_treatments
    else:
        return False
