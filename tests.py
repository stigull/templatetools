#! /usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from datetime import datetime, date

from utils.dateformatting import NEFNIFALL, THOLFALL, THAGUFALL, EIGNARFALL

from templatetools.templatetags.templatetools import format_datetime, readable_nr_of_comments
from templatetools.templatetags.templatetools import format_phone, format_age, format_date

class FormatDateTimeTestCase(unittest.TestCase):

    def test_format_datetime(self):
        YESTERDAY = u"Í gær, þriðjudaginn 21. október 2008, kl. 20:01"
        TODAY = u"Í dag, miðvikudaginn 22. október 2008, kl. 10:01"
        TOMORROW = u"Á morgun, fimmtudaginn 23. október 2008, kl. 23:00"
        NEXT = u"Föstudaginn 24. október 2008, kl. 13:00"

        now_date = date(2008,10,22)

        self.assertEqual(format_datetime(datetime(2008, 10, 21, 20, 01), now_date), YESTERDAY)
        self.assertEqual(format_datetime(datetime(2008, 10, 22, 10, 01), now_date), TODAY)
        self.assertEqual(format_datetime(datetime(2008, 10, 23, 23, 00), now_date), TOMORROW)
        self.assertEqual(format_datetime(datetime(2008, 10, 24, 13, 00), now_date), NEXT)

class ReadableNrOfCommentsTestCase(unittest.TestCase):
    def test_no_comments(self):
        self.assertEqual(readable_nr_of_comments(0), u"Engin athugasemd")

    def test_one_comment(self):
        self.assertEqual(readable_nr_of_comments(1), u"Ein athugasemd")

    def test_many_comments(self):
        self.assertEqual(readable_nr_of_comments(2), u"2 athugasemdir")

    def test_negative_comments(self):
        self.assertEqual(readable_nr_of_comments(-1), u"")

class FormatPhoneTestCase(unittest.TestCase):
    def test_format_phone(self):
        self.assertEqual(format_phone(u"5688223"), u"568-8223")

    def test_format_phone_formatted(self):
        self.assertEqual(format_phone(u"568-8223"), u"568-8223")

class FormatAgeTestCase(unittest.TestCase):
    def test_exactly_years(self):
        self.assertEqual(format_age((20,0,0)), u"20 ára")
        self.assertEqual(format_age((21,0,0)), u"21 árs")
        self.assertEqual(format_age((31,0,0)), u"31 árs")

    def test_exactly_years_and_months(self):
        self.assertEqual(format_age((20,1,0)), u"20 ára og 1 mánaða")

    def test_exactly_years_and_days(self):
        self.assertEqual(format_age((20,0,1)), u"20 ára og 1 dags")
        self.assertEqual(format_age((21,0,2)), u"21 árs og 2 daga")
        self.assertEqual(format_age((20,0,21)),u"20 ára og 21 daga")

class FormatDateTestCase(unittest.TestCase):
    def test_format_date_nf(self):
        self.assertEqual(format_date(date(2008, 12, 22), NEFNIFALL),
            u"mánudagurinn 22. desember 2008")

    def test_format_date_tf(self):
        self.assertEqual(format_date(date(2008, 12, 22), THOLFALL),
            u"mánudaginn 22. desember 2008")

    def test_format_date_tgf(self):
        self.assertEqual(format_date(date(2008, 12, 22), THAGUFALL),
            u"mánudeginum 22. desember 2008")

    def test_format_date_ef(self):
         self.assertEqual(format_date(date(2008, 12, 22), EIGNARFALL),
            u"mánudagsins 22. desember 2008")

if __name__ == "__main__":
    unittest.main()
