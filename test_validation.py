import unittest
from hamcrest import *
from datetime import date

from validation import validate_date_sequence, validate_treatment_delay, validate_treatment_type


class TestValidateDateSequence(unittest.TestCase):
    def setUp(self):
        self.date_first_seen = date(year=2018, month=1, day=1)
        self.diagnosis_date = date(year=2018, month=2, day=2)
        self.treatment_start = date(year=2018, month=3, day=3)
        self.treatment_end = date(year=2018, month=4, day=4)

    def test_validate_date_sequence_valid(self):
        is_valid_sequence = validate_date_sequence(self.date_first_seen, self.diagnosis_date,
                                                   self.treatment_start, self.treatment_end)
        assert_that(is_valid_sequence, equal_to(True))

    def test_validate_date_sequence_invalid_first_seen_after_diagnosis(self):
        self.date_first_seen = date(year=2018, month=2, day=3)
        is_valid_sequence = validate_date_sequence(self.date_first_seen, self.diagnosis_date,
                                                   self.treatment_start, self.treatment_end)
        assert_that(is_valid_sequence, equal_to(False))

    def test_validate_date_sequence_invalid_first_seen_after_treatment_start(self):
        self.date_first_seen = date(year=2018, month=3, day=4)
        is_valid_sequence = validate_date_sequence(self.date_first_seen, self.diagnosis_date,
                                                   self.treatment_start, self.treatment_end)
        assert_that(is_valid_sequence, equal_to(False))

    def test_validate_date_sequence_invalid_first_seen_after_treatment_end(self):
        self.date_first_seen = date(year=2018, month=4, day=5)
        is_valid_sequence = validate_date_sequence(self.date_first_seen, self.diagnosis_date,
                                                   self.treatment_start, self.treatment_end)
        assert_that(is_valid_sequence, equal_to(False))

    def test_validate_date_sequence_invalid_diagnosis_not_between_first_seen_and_treatment_start(self):
        self.diagnosis_date = date(year=2018, month=3, day=4)
        is_valid_sequence = validate_date_sequence(self.date_first_seen, self.diagnosis_date,
                                                   self.treatment_start, self.treatment_end)
        assert_that(is_valid_sequence, equal_to(False))

    def test_validate_date_sequence_invalid_treatment_end_before_diagnosis(self):
        self.treatment_end = date(year=2018, month=2, day=1)
        is_valid_sequence = validate_date_sequence(self.date_first_seen, self.diagnosis_date,
                                                   self.treatment_start, self.treatment_end)
        assert_that(is_valid_sequence, equal_to(False))

    def test_validate_date_sequence_invalid_treatment_end_before_treatment_start(self):
        self.treatment_end = date(year=2018, month=3, day=1)
        is_valid_sequence = validate_date_sequence(self.date_first_seen, self.diagnosis_date,
                                                   self.treatment_start, self.treatment_end)
        assert_that(is_valid_sequence, equal_to(False))


class TestValidateTreatmentDelayAdultPatient(unittest.TestCase):
    def setUp(self):
        self.is_child_patient = False
        self.diagnosis_date = date(year=2014, month=1, day=1)
        self.treatment_start_date = date(year=2014, month=2, day=1)

    def test_validate_treatment_delay_valid_under_60_days(self):
        is_valid_delay = validate_treatment_delay(self.diagnosis_date, self.treatment_start_date,
                                                  self.is_child_patient)
        assert_that(is_valid_delay, equal_to(True))

    def test_validate_treatment_delay_valid_on_60_days(self):
        self.treatment_start_date = date(year=2014, month=3, day=2)
        is_valid_delay = validate_treatment_delay(self.diagnosis_date, self.treatment_start_date,
                                                  self.is_child_patient)
        assert_that(is_valid_delay, equal_to(True))

    def test_validate_treatment_delay_invalid_over_60_days(self):
        self.treatment_start_date = date(year=2014, month=3, day=3)
        is_valid_delay = validate_treatment_delay(self.diagnosis_date, self.treatment_start_date,
                                                  self.is_child_patient)
        assert_that(is_valid_delay, equal_to(False))


class TestValidateTreatmentDelayChildPatient(unittest.TestCase):
    def setUp(self):
        self.is_child_patient = True
        self.diagnosis_date = date(year=1997, month=1, day=1)
        self.treatment_start_date = date(year=1997, month=1, day=29)

    def test_validate_treatment_delay_valid_under_30_days(self):
        is_valid_delay = validate_treatment_delay(self.diagnosis_date, self.treatment_start_date,
                                                  self.is_child_patient)
        assert_that(is_valid_delay, equal_to(True))

    def test_validate_treatment_delay_valid_on_30_days(self):
        self.treatment_start_date = date(year=1997, month=1, day=30)
        is_valid_delay = validate_treatment_delay(self.diagnosis_date, self.treatment_start_date,
                                                  self.is_child_patient)
        assert_that(is_valid_delay, equal_to(True))

    def test_validate_treatment_delay_invalid_over_30_days(self):
        self.treatment_start_date = date(year=1997, month=2, day=1)
        is_valid_delay = validate_treatment_delay(self.diagnosis_date, self.treatment_start_date,
                                                  self.is_child_patient)
        assert_that(is_valid_delay, equal_to(False))


class TestValidateTreatmentTypeForType3Cancer(unittest.TestCase):
    def setUp(self):
        self.cancer_type = 3

    def test_validate_treatment_type_valid_treatment_type_3(self):
        self.treatment_type = 3
        is_valid_treatment_type = validate_treatment_type(self.cancer_type, self.treatment_type)
        assert_that(is_valid_treatment_type, equal_to(True))

    def test_validate_treatment_type_valid_treatment_type_4(self):
        self.treatment_type = 4
        is_valid_treatment_type = validate_treatment_type(self.cancer_type, self.treatment_type)
        assert_that(is_valid_treatment_type, equal_to(True))

    def test_validate_treatment_type_valid_treatment_type_5(self):
        self.treatment_type = 5
        is_valid_treatment_type = validate_treatment_type(self.cancer_type, self.treatment_type)
        assert_that(is_valid_treatment_type, equal_to(True))

    def test_validate_treatment_type_invalid_treatment_type_1(self):
        self.treatment_type = 1
        is_valid_treatment_type = validate_treatment_type(self.cancer_type, self.treatment_type)
        assert_that(is_valid_treatment_type, equal_to(False))

    def test_validate_treatment_type_invalid_treatment_type_2(self):
        self.treatment_type = 2
        is_valid_treatment_type = validate_treatment_type(self.cancer_type, self.treatment_type)
        assert_that(is_valid_treatment_type, equal_to(False))


class TestValidateTreatmentTypeForType4Cancer(unittest.TestCase):
    def setUp(self):
        self.cancer_type = 4

    def test_validate_treatment_type_valid_treatment_type_1(self):
        self.treatment_type = 1
        is_valid_treatment_type = validate_treatment_type(self.cancer_type, self.treatment_type)
        assert_that(is_valid_treatment_type, equal_to(True))

    def test_validate_treatment_type_valid_treatment_type_2(self):
        self.treatment_type = 2
        is_valid_treatment_type = validate_treatment_type(self.cancer_type, self.treatment_type)
        assert_that(is_valid_treatment_type, equal_to(True))

    def test_validate_treatment_type_invalid_treatment_type_3(self):
        self.treatment_type = 3
        is_valid_treatment_type = validate_treatment_type(self.cancer_type, self.treatment_type)
        assert_that(is_valid_treatment_type, equal_to(False))

    def test_validate_treatment_type_invalid_treatment_type_4(self):
        self.treatment_type = 4
        is_valid_treatment_type = validate_treatment_type(self.cancer_type, self.treatment_type)
        assert_that(is_valid_treatment_type, equal_to(False))

    def test_validate_treatment_type_invalid_treatment_type_5(self):
        self.treatment_type = 5
        is_valid_treatment_type = validate_treatment_type(self.cancer_type, self.treatment_type)
        assert_that(is_valid_treatment_type, equal_to(False))
