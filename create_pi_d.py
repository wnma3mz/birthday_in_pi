# coding: utf-8
import json
import time

import pandas as pd
from tqdm import tqdm

from read_large_pi import m1


def create_pi_date_txt(start_date, gap, fname):
    date_list = pd.date_range(start=start_date, periods=gap).strftime("%Y%m%d").tolist()
    if os.path.isfile("pi.json"):
        with open("pi.json", "r") as f:
            date_digits_d = json.load(f)
        date_list = [
            date for date in date_list if str(date) not in date_digits_d.keys()
        ]
    with open(fname, "a+", encoding="utf-8") as f:
        for date in tqdm(date_list):
            f.write("{}:{}\n".format(date, m1(date)))


def create_pi_date_json(fname):
    with open(fname, "r", encoding="utf-8") as f:
        data = f.readlines()
    d = {line.split(":")[0]: line.split(":")[1].strip() for line in data}
    with open("pi.json", "w") as f:
        json.dump(d, f)


def test_pi_date_json(target_str):
    s1 = time.time()
    with open("pi.json", "r") as f:
        data = json.load(f)
    if target_str in data.keys():
        print(data[target_str])
    print(time.time() - s1)


if __name__ == "__main__":
    start_date = "19700101"
    gap = 365 * 50
    fname = "pi_date.txt"
    create_pi_date_txt(start_date, gap, fname)
    create_pi_date_json(fname)

    target_str = "20010102"
    test_pi_date_json(target_str)
