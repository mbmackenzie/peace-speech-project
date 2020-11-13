import os

from typing import List, Dict

ORIGINAL_DATA_FOLDER = os.path.join("data", "original")
RAW_DATA_FOLDER = os.path.join("data", "raw")
SAMPLE_RAW_DATA_FOLDER = os.path.join("data", "sample_raw")
CLEAN_DATA_FOLDER = os.path.join("data", "clean")

PEACEFUL_COUNTRIES = ["AU", "CA", "IE", "NZ", "SG", "GB"]
NONPEACEFUL_COUNTRIES = ["BD", "KE", "NG", "PK", "TZ"]


def get_country_labels(peaceful: List[str] = None,
                       nonpeaceful: List[str] = None):

    return {
        "peaceful": peaceful if peaceful else PEACEFUL_COUNTRIES,
        "nonpeaceful": nonpeaceful if nonpeaceful else NONPEACEFUL_COUNTRIES
    }


def get_society_label(country: str, country_labels: Dict, default: str = "Other"):
    for label, countries in country_labels.items():
        if country in countries:
            return label.title()

    return default
