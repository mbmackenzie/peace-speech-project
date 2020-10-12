import os
import re
import glob
import codecs
import pathlib

from typing import List, Tuple

import numpy as np
import pandas as pd

# from utils.clean import clean_text


def clean_text(text: str) -> str:
    return text.strip()


# CONSTANTS
RAW_DATA_FOLDER = os.path.join("data", "raw")
CLEAN_DATA_FOLDER = os.path.join("data", "clean")

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


def get_sources_files() -> List[str]:
    return glob.glob(os.path.join(RAW_DATA_FOLDER, "*sources*.txt"))


def get_text_folders() -> List[str]:
    return glob.glob(os.path.join(RAW_DATA_FOLDER, "*/"))


def get_text_files(folder="*") -> List[str]:
    return glob.glob(os.path.join(RAW_DATA_FOLDER, folder, "*.txt"))


def read_sources_file(file_path: str, clean=True) -> pd.DataFrame:
    # data is separated by 1 or 2 tabs
    sources = pd.read_csv(
        file_path, sep="\t{1,2}", header=None, encoding="ISO-8859-1", engine='python'
    )

    sources.columns = SOURCES_COLUMNS

    if clean:
        _clean_sources_file(sources)

    return sources


def get_text_file_path(text_folders: List[str], year: int, month: int, country: str) -> str:
    folder = _match_folder(text_folders, year, month,
                           path_cleaner=_get_last_path_element)

    text_files = get_text_files(folder=folder)
    file_name = _match_file(text_files, year, month, country,
                            path_cleaner=_get_last_path_element)

    path = os.path.join(RAW_DATA_FOLDER, folder, file_name)
    return path


def read_text_file(file_path: str) -> pd.DataFrame:
    # find lines that start with @@, extract id and text from them
    with open(file_path, "r") as f:
        text = pd.DataFrame(
            [re.search("(\d+)\s(.*)", l[2:]).groups()
             for l in f.readlines() if l.startswith("@@")],
            columns=["id", "text"]
        )
        f.close()

    # id should be an integer
    text["id"] = text["id"].astype(int)
    text["text"] = text["text"].apply(clean_text)

    return text


def get_report_folder(report: pd.Series) -> str:
    """Get the folder a report belongs in as COUNTRY/YEAR"""
    if not pd.isna(report.date):
        year = report.date.strftime("%Y")
        return f"{report.country}/{year}"
    else:
        return f"{report.country}"


def get_report_name(report: pd.Series) -> str:
    """Get the file name for a report as ID_COUNTRY_DATE.txt"""
    if not pd.isna(report.date):
        date_string = report.date.strftime("%d-%m-%y")
        return f"{report.id}_{report.country}_{date_string}.txt"
    else:
        return f"{report.id}_{report.country}.txt"


def export_report(report: pd.Series, path=None) -> str:
    """Export a report to the correct folder with the correct name

    Keyword Arguments:
        path {str, optional}: a parent path to the folder. The directory you want the data all saved to.

    Returns:
        the output path FOLDER/FILE.txt, excluding the path argument.
    """
    folder = get_report_folder(report)
    file = get_report_name(report)

    full_path = f"{path + '/' if path else ''}{folder}"

    # create the folder, if it doesn't already exist
    pathlib.Path(full_path).mkdir(parents=True, exist_ok=True)

    # write the file
    with codecs.open(f"{full_path}/{file}", "w", "ISO-8859-1") as f:
        if not pd.isna(report.text):
            title = report.title if not pd.isna(report.title) else ""
            website = report.website if not pd.isna(report.title) else ""
            url = report.url if not pd.isna(report.url) else ""
            f.writelines([title, "\n", website, "\n",
                          url, "\n\n", report.text])
        f.close()

    return f"{folder}/{file}"


def get_basic_summary_stats(df: pd.DataFrame) -> Tuple[int, int, int]:
    num_articles = df.shape[0]
    total_words = int(df["n_words"].astype(float).sum(skipna=True))
    num_sources = df["website"].unique().shape[0]

    return num_sources, num_articles, total_words


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


def _match_file(files: List[str], year: int, month: int, country: int, path_cleaner=None) -> str:
    for file in files:

        if path_cleaner:
            file = path_cleaner(file)

        split_loc = _split_location(file)
        if split_loc[0] == "text":
            f_year, f_month, f_country = split_loc[1:-1]
        else:
            f_year, f_month, f_country = split_loc[:-1]

        if format_year(year) == f_year and format_month(month) == f_month and country.lower() == f_country.lower():
            return file


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

    # date n_words -> int/nan

    # date column -> pandas.DateTime
    sources["date"] = pd.to_datetime(sources["date"], format="%y-%m-%d")
