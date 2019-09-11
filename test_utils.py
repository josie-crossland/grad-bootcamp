import unittest
from hamcrest import assert_that, equal_to
from datetime import datetime
from dateutil.relativedelta import relativedelta

from utils import get_is_child_patient


class TestGetIsChildPatient(unittest.TestCase):
    def test_get_is_child_patient_returns_true_if_under_sixteen_years(self):
        patient_age_in_years = 15
        self.date_of_birth = _create_relative_date_of_birth(patient_age_in_years)
        is_child_patient = get_is_child_patient(self.date_of_birth)
        assert_that(is_child_patient, equal_to(True))

    def test_get_is_child_patient_returns_false_if_sixteen_years(self):
        patient_age_in_years = 16
        self.date_of_birth = _create_relative_date_of_birth(patient_age_in_years)
        is_child_patient = get_is_child_patient(self.date_of_birth)
        assert_that(is_child_patient, equal_to(False))

    def test_get_is_child_patient_returns_false_if_over_sixteen_years(self):
        patient_age_in_years = 17
        self.date_of_birth = _create_relative_date_of_birth(patient_age_in_years)
        is_child_patient = get_is_child_patient(self.date_of_birth)
        assert_that(is_child_patient, equal_to(False))


def _create_relative_date_of_birth(age):
    return datetime.now() - relativedelta(years=age)
