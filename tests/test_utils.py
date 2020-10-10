import os
import unittest

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

import utils
from utils.utils import _get_raw_path


class TestUtilityFunctions(unittest.TestCase):

    def test_get_raw_path_no_extension(self):
        """Get the correct folder path"""
        self.assertEqual(_get_raw_path("test"),
                         os.path.join("data", "raw", "test"))

    def test_get_raw_path_with_extension(self):
        """Get the correct text file path"""
        self.assertEqual(_get_raw_path("test", extension=".txt"),
                         os.path.join("data", "raw", "test.txt"))

    def test_get_sources_files(self):
        source_files = utils.get_sources_files()
        self.assertTrue(
            all(["sources" in f and f.endswith(".txt") for f in source_files]))

    def test_read_sources_file(self):
        """Sources tables are read in properly"""
        test_path = os.path.join("tests", "res", "test_sources.txt")
        test_sources = utils.read_sources_file(test_path, explicit_path=True)

        self.assertEqual(test_sources.shape, (2, len(utils.SOURCES_COLUMNS)))
        self.assertEqual(test_sources.loc[0, "website"], "Google")
        self.assertTrue(is_datetime(test_sources["date"]))
