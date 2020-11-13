import os
import glob
import time
import pathlib
from datetime import datetime

from typing import List

from tqdm import tqdm
import pandas as pd

from .common import (
    CLEAN_DATA_FOLDER
)


# Public Function

def read_all_files(path: str = None,
                   countries: List[str] = None,
                   sample: int = None,
                   get_details: bool = True):

    if not countries:
        countries = get_countries(path=path)

    article_paths = []
    for country in tqdm(countries,  desc="Finding files..."):
        article_paths.append(pd.Series(get_files(country, path=path)))

    articles = pd.concat(article_paths).rename("path")

    time.sleep(.2)

    print(f"\n{articles.shape[0]:,d} articles found.")
    if sample:
        sample = articles.shape[0] if articles.shape[0] < sample else sample
        print(f"Sampling {sample} random articles.\n")
        articles = articles.sample(sample)
    else:
        print()

    time.sleep(.2)

    if get_details:
        tqdm.pandas(desc="Getting details")
        path_details = articles.progress_apply(
            get_details_from_path).reset_index(drop=True)
        return path_details.join(articles.reset_index(drop=True))
    else:
        return articles


def get_text(files_df: pd.DataFrame, path: str = None) -> pd.DataFrame:
    tqdm.pandas(desc="Getting text")
    text = files_df.path.progress_apply(get_text_from_file, path=path)

    return files_df.join(text)


def get_countries(path: str = None) -> List[str]:
    if not path:
        path = CLEAN_DATA_FOLDER

    country_folders = glob.glob(os.path.join(path, "*/"))
    return [pathlib.Path(x).parts[-1] for x in country_folders]


def get_files(country: str, publisher="*", year="*", path: str = None) -> List[str]:
    if not path:
        path = CLEAN_DATA_FOLDER

    text_files = glob.glob(os.path.join(
        path, country, publisher, year, "*.txt"))
    return [os.path.join(*pathlib.Path(x).parts[-4:]) for x in text_files]


def get_details_from_path(file_path: str) -> pd.Series:
    parts = pathlib.Path(file_path).parts[-4:]
    extra = __clean_file_name(parts[-1])
    names = ["country", "publisher", "year", "month", "id"]
    return pd.Series(
        (*parts[:-1], *extra),
        index=names
    )


def get_text_from_file(file_path: str, path: str = None):
    if not path:
        path = CLEAN_DATA_FOLDER

    with open(os.path.join(path, file_path), "r", encoding="ISO-8859-1") as f:
        lines = f.readlines()
        f.close()

    title = lines[1].strip()
    text = lines[-1].strip()

    return pd.Series(
        (title, text),
        index=["title", "text"]
    )


# Private Funtions

def __clean_file_name(file_name: str) -> str:
    id_, _, date = file_name[:-4].split("_")
    month = datetime.strptime(date, "%d-%m-%y").month
    return (month, id_)
