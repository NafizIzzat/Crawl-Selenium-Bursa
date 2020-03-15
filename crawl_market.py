# -*- coding: utf-8 -*-

"""
To crawl the stock market every page and store in csv
"""

__author__ = 'MNI'
__version__ = '1.0'

from pathlib import Path, PurePath
import sys
import logging
from time import time
from selenium import webdriver
from time import sleep


def logger():
    path_logger = f"{Path(__file__).absolute()}"
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s : %(levelname)s : %(message)s',
                        datefmt='%d-%m-%Y %I:%M:%S %p')
    logging.root.setLevel(level=logging.INFO)
    logging.info(f"Running {path_logger}")
    return logging.getLogger(path_logger)


def driver():
    return webdriver.Chrome(executable_path=f"{Path.cwd()}/driver/chromedriver")


def data(parts):
    return [x.text for x in run_chrome.find_element_by_id('DataTables_Table_0_wrapper')
                                      .find_elements_by_class_name(parts)]


def max_page():
    return int([x.text for x in run_chrome.find_element_by_class_name("pagination")
                                          .find_elements_by_tag_name("li")][-2])


def clean(raw_data):
    for y in raw_data:
        clean_data = y.replace("\n", " ").replace("\"", "").replace(",", "").replace("[", "").replace("]", "").replace("+", "")
        split_data = clean_data.split()
        datalist.append(split_data)


if __name__ == "__main__":
    t0 = time()
    log = logger()
    page = 1
    datalist = []
    url = "https://www.bursamalaysia.com/market_information/shariah_compliant_equities_prices?per_page=50"

    run_chrome = driver()
    open_url = run_chrome.get(url)

    while True:
        if page == max_page():
            log.info("all data collected")
            break
        else:
            current_url = run_chrome.current_url
            new_url = run_chrome.get(f"{url}&page={page}")
            clean(data('odd') + data('even'))
            page += 1
        continue

    run_chrome.close()
    t1 = time()
    timer = t1-t0
    print(timer)
