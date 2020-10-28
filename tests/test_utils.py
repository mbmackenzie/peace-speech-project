import os
import re
import unittest

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

import utils
from utils.utils import (
    _get_last_path_element,
    _split_location,
    _get_raw_path,
    _match_folder,
    _match_file
)


class TestPublicUtilityFunctions(unittest.TestCase):

    def test_format_year(self):
        """A four digit year should return a the last 2 digits as a string"""
        # 2012 should be 12
        self.assertEqual(utils.format_year(2012), "12")

        # 2004 should be 04
        self.assertEqual(utils.format_year(2004), "04")

        # 2020 should be 20
        self.assertEqual(utils.format_year(2020), "20")

    def test_format_month(self):
        """A month integer should return a 2 digit string"""
        # 1 should be 01
        self.assertEqual(utils.format_month(1), "01")

        # 12 should be 12
        self.assertEqual(utils.format_month(12), "12")

    def test_get_sources_files(self):
        """The files are actually sources files"""
        source_files = utils.get_sources_files()
        check = all(["sources" in f and f.endswith(".txt")
                     for f in source_files])
        self.assertTrue(check)

    def test_read_sources_file(self):
        """Sources tables are read in properly"""
        test_path = os.path.join("tests", "res", "test_sources.txt")
        test_sources = utils.read_sources_file(test_path)

        self.assertEqual(test_sources.shape, (2, len(utils.SOURCES_COLUMNS)))
        self.assertEqual(test_sources.loc[0, "website"], "Google")
        self.assertTrue(is_datetime(test_sources["date"]))

    def test_get_text_folders(self):
        text_folders = utils.get_text_folders()
        check = all([re.search(r"text[\-\_]\d\d[\-\_]\d\d", f)
                     for f in text_folders])
        self.assertTrue(check)


class TestPrivateUtilityFunctions(unittest.TestCase):

    def test__get_last_path_part(self):
        path = os.path.join("path", "to", "folder")
        last_part = _get_last_path_element(path)

        self.assertEqual(last_part, "folder")

    def test__split_location(self):
        # a-b-c-d -> [a, b, c, d]
        self.assertEqual(_split_location("a-b-c-d"), list("abcd"))

        # a_b-c.d -> [a, b, c, d]
        self.assertEqual(_split_location("a_b-c.d"), list("abcd"))

        # ab_cd -> [ab, cd]
        self.assertEqual(_split_location("ab_cd"), ["ab", "cd"])

    def test__get_raw_path_no_extension(self):
        """Get the correct folder path"""
        self.assertEqual(_get_raw_path("test"),
                         os.path.join("data", "raw", "test"))

    def test__get_raw_path_with_extension(self):
        """Get the correct text file path"""
        self.assertEqual(_get_raw_path("test", extension=".txt"),
                         os.path.join("data", "raw", "test.txt"))

    def test__match_folder(self):
        year, month = 2020, 10
        folders = [
            "text-20_07",
            "text_18-10",
            "text-20-10"
        ]

        folder = _match_folder(folders, year, month)
        self.assertEqual(folder, folders[-1])

    def test__match_file__no_match(self):
        year, month, country = 2020, 10, "US"
        files = [
            "text-20_07_US.txt",
            "text_18-10_AU.txt",
            "text-20-11-US.txt"
        ]

        file_name = _match_file(files, year, month, country)
        self.assertIsNone(file_name)

    def test__match_file__one_match(self):
        year, month, country = 2020, 10, "US"
        files = [
            "text-20_07_US.txt",
            "text_18-10_AU.txt",
            "text-20-10-US.txt"
        ]

        file_name = _match_file(files, year, month, country)
        self.assertTrue(isinstance(file_name, list))
        self.assertEqual(file_name, [files[-1]])

    def test__match_file__multiple_matches(self):
        year, month, country = 2020, 10, "US"
        files = [
            "text-20_07_US.txt",
            "text_18-10_AU.txt",
            "text-20-10-US1.txt",
            "text-20-10-us2.txt"
        ]

        file_names = _match_file(files, year, month, country)
        self.assertTrue(isinstance(file_names, list))
        self.assertEqual(file_names, files[-2:])
