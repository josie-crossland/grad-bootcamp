import unittest
from hamcrest import assert_that, equal_to
from datetime import date

from utils import get_is_child_patient


class TestGetIsChildPatient(unittest.TestCase):
    def setUp(self):
        self.date_first_seen = date(year=2019, month=9, day=17)

    def test_get_is_child_patient_returns_true_if_under_sixteen_years(self):
        self.date_of_birth = date(year=2004, month=8, day=5)
        is_child_patient = get_is_child_patient(self. date_first_seen, self.date_of_birth)
        assert_that(is_child_patient, equal_to(True))

    def test_get_is_child_patient_returns_false_if_sixteen_years(self):
        self.date_of_birth = date(year=2003, month=8, day=5)
        is_child_patient = get_is_child_patient(self.date_first_seen, self.date_of_birth)
        assert_that(is_child_patient, equal_to(False))

    def test_get_is_child_patient_returns_false_if_over_sixteen_years(self):
        self.date_of_birth = date(year=2002, month=8, day=5)
        is_child_patient = get_is_child_patient(self. date_first_seen, self.date_of_birth)
        assert_that(is_child_patient, equal_to(False))
