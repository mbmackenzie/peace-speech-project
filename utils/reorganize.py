import os
import re
import glob
import codecs
import pathlib

from typing import List, Tuple

import numpy as np
import pandas as pd

from slugify import slugify

from .common import (
    RAW_DATA_FOLDER
)

# from utils.clean import clean_text


def clean_text(text: str) -> str:
    return text.strip()


# CONSTANTS


SOURCES_COLUMNS = [
    "id",
    "n_words",
    "date",
    "country",
    "website",
    "url",
    "title"
]


# PUBLIC FUNCTIONS


def format_year(year: int) -> str:
    return str(year)[2:]


def format_month(month: int) -> str:
    return f"{month:02d}"


def get_sources_files(path: str = None) -> List[str]:
    if not path:
        path = RAW_DATA_FOLDER
    return glob.glob(os.path.join(path, "*sources*.txt"))


def get_text_folders(path: str = None) -> List[str]:
    if not path:
        path = RAW_DATA_FOLDER
    return glob.glob(os.path.join(path, "*/"))


def get_text_files(path: str = None, folder: str = "*") -> List[str]:
    if not path:
        path = RAW_DATA_FOLDER

    return glob.glob(os.path.join(path, folder, "*.txt"))


def read_sources_file(file_path: str, clean=True) -> pd.DataFrame:
    # data is separated by 1 or 2 tabs
    sources = pd.read_csv(
        file_path, sep="\t{1,2}", header=None, encoding="ISO-8859-1", engine='python'
    )

    sources.columns = SOURCES_COLUMNS

    if clean:
        _clean_sources_file(sources)

    return sources


def get_text_file_paths(text_folders: List[str], year: int, month: int, country: str, path: str = None) -> str:
    if not path:
        path = RAW_DATA_FOLDER

    folder = _match_folder(text_folders, year, month,
                           path_cleaner=_get_last_path_element)

    text_files = get_text_files(path=path, folder=folder)
    file_names = _match_file(text_files, year, month, country,
                             path_cleaner=_get_last_path_element)

    if not file_names:
        return None

    return [os.path.join(path, folder, file_name)
            for file_name in file_names]


def read_text_file(file_path: str) -> pd.DataFrame:
    # find lines that start with @@, extract id and text from them
    bad_lines = []
    with open(file_path, "r") as f:
        lines = f.readlines()

        try:
            text = pd.DataFrame(
                [re.search(r"(\d+)\s(.*)", l[2:]).groups()
                 for l in lines if l.startswith("@@")],
                columns=["id", "text"]
            )

        except:
            text = pd.DataFrame(
                [re.search(r"(\d+)\s(.*)", l[2:]).groups()
                 for l in lines if l.startswith("@@") and re.match(r"(\d+)\s(.*)", l[2:])],
                columns=["id", "text"]
            )

            bad_lines = [l for l in lines
                         if l.startswith("@@") and not re.match(r"(\d+)\s(.*)", l[2:])]

        f.close()

    # id should be an integer
    text["id"] = text["id"].astype(int)
    text["text"] = text["text"].apply(clean_text)

    return text, bad_lines


def get_report_folder(report: pd.Series) -> str:
    """Get the folder a report belongs in as COUNTRY/YEAR"""
    publisher = slugify(
        report.website if not pd.isna(report.website) else "No Publisher"
    )

    if not pd.isna(report.date):
        year = report.date.strftime("%Y")
        return os.path.join(report.country, publisher, year)
    else:
        os.path.join(report.country, publisher)


def get_report_name(report: pd.Series) -> str:
    """Get the file name for a report as ID_COUNTRY_DATE.txt"""
    if not pd.isna(report.date):
        date_string = report.date.strftime("%d-%m-%y")
        return f"{report.id}_{report.country}_{date_string}.txt"
    else:
        return f"{report.id}_{report.country}.txt"


def export_report(report: pd.Series, path=None, execute=True) -> str:
    """Export a report to the correct folder with the correct name

    Keyword Arguments:
        path {str, optional}: a parent path to the folder. The directory you want the data all saved to.

    Returns:
        the output path FOLDER/FILE.txt, excluding the path argument.
    """
    folder = get_report_folder(report)
    file_name = get_report_name(report)

    full_path = os.path.join(path, folder) if path else folder

    # create the folder, if it doesn't already exist
    pathlib.Path(full_path).mkdir(parents=True, exist_ok=True)

    # write the file if execute
    if execute:
        with codecs.open(f"{full_path}/{file_name}", "w", "ISO-8859-1") as f:
            id_number = str(report.id) if not pd.isna(report.id) else ""
            title = report.title if not pd.isna(report.title) else ""
            website = report.website if not pd.isna(report.title) else ""
            url = report.url if not pd.isna(report.url) else ""
            f.writelines([id_number, "\n",
                          title, "\n",
                          website, "\n",
                          url, "\n\n", report.text])
            f.close()

    return os.path.join(folder, file_name)


def get_basic_summary_stats(df: pd.DataFrame) -> Tuple[int, int, int]:
    num_articles = df.shape[0]
    total_words = int(df["n_words"].astype(float).sum(skipna=True))

    return num_articles, total_words


# PRIVATE FUNCTIONS

def _get_country_or_na(country_code: str) -> str:
    return country_code if re.match("[A-Za-z]{2}", country_code) else pd.NA


def _get_last_path_element(path: str):
    return pathlib.Path(path).parts[-1]


def _split_location(loc: str) -> str:
    return re.split(r"[\-\_\.]", loc)


def _get_raw_path(name: str, extension="") -> str:
    return os.path.join(RAW_DATA_FOLDER, name + extension)


def _match_folder(folders: List[str], year: int, month: int, path_cleaner=None) -> str:
    for folder in folders:

        if path_cleaner:
            folder = path_cleaner(folder)

        _, f_year, f_month = _split_location(folder)
        if format_year(year) == f_year and format_month(month) == f_month:
            return folder


def _match_file(files: List[str], year: int, month: int, country: int, path_cleaner=None) -> List[str]:
    matched_files = []
    for text_file in files:
        if path_cleaner:
            text_file = path_cleaner(text_file)

        split_loc = _split_location(text_file)
        if split_loc[0] == "text":
            f_year, f_month, f_country = split_loc[1:-1]
        else:
            f_year, f_month, f_country = split_loc[:-1]

        if f_country[-1].isdigit():
            f_country = f_country[:-1]

        if format_year(year) == f_year and format_month(month) == f_month and country.lower() == f_country.lower():
            matched_files.append(text_file)

    if len(matched_files) == 0:
        return None

    return matched_files


def _check_sources_needs_shift(sources: pd.DataFrame) -> bool:
    possible_shift = sources[sources.title.isna()]
    return not pd.api.types.is_integer_dtype(possible_shift.n_words)


def _shift_sources(sources: pd.DataFrame):
    shift_idx = sources[sources.title.isna()].copy().index
    sources.iloc[shift_idx, 1:] = sources.iloc[shift_idx, 1:].shift(axis=1)


def _clean_sources_file(sources: pd.DataFrame):
    # country column only allows 2 char country codes
    sources["country"] = sources.country.apply(_get_country_or_na)

    # is there a column parse error?
    if _check_sources_needs_shift(sources):
        _shift_sources(sources)

    # strip website
    sources["website"] = sources["website"].str.strip()

    # n_words date-> int/nan
    # TODO

    # date column -> pandas.DateTime
    sources["date"] = pd.to_datetime(sources["date"], format="%y-%m-%d")
