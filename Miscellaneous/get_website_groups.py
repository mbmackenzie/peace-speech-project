import numpy as np
import pandas as pd

import binpacking

reports = pd.read_csv("data/clean/all_reports.csv")
websites = reports.website.value_counts()

pct_of_data = (websites / websites.sum()).cumsum()
use_sites = websites[pct_of_data[pct_of_data < .25].index.tolist()]

bins = binpacking.to_constant_bin_number(use_sites.to_dict(), 4)


def print_bin(bin):
    num_articles = np.sum(list(bin.values()))
    websites = list(bin.keys())
    print(f"Num Articles: {num_articles} - Websites: {websites}")


for b in bins:
    print_bin(b)
    print()
