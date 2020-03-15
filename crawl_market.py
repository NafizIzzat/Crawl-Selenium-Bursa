# -*- coding: utf-8 -*-

"""
To crawl the stock market and put in mysql
"""

__author__ = 'MNI'
__version__ = '1.0'

from pathlib import Path
import sys
import logging
from time import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import mysql.connector
from time import sleep
from datetime import datetime


def logger():
    path_logger = f"{Path(__file__).absolute()}"
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s : %(levelname)s : %(message)s',
                        datefmt='%d-%m-%Y %I:%M:%S %p')
    logging.root.setLevel(level=logging.INFO)
    logging.info(f"Running {path_logger}")
    return logging.getLogger(path_logger)


def driver():
    options = Options()
    options.headless = True
    return webdriver.Firefox(executable_path=f"{Path.cwd()}/geckodriver", options=options)


def data(parts):
    return [x.text for x in run_driver.find_element_by_id('DataTables_Table_0_wrapper')
            .find_elements_by_class_name(parts)]


def max_page():
    return int([x.text for x in run_driver.find_element_by_class_name("pagination")
            .find_elements_by_tag_name("li")][-2])


# get current time - 01-01-2019 23:59:59
def current_time():
    dt = datetime.now()
    dt = dt.strftime("%Y-%m-%dT%H:%M:%S")
    return dt


# get current time (epoch)
def current_epoch():
    dt = datetime.now()
    dt = int(dt.strftime("%s")) * 1000
    return dt


if __name__ == "__main__":
    t0 = time()
    log = logger()

    # set mysql parameters
    mydb = mysql.connector.connect(
        host="localhost",
        user="nafizizzat",
        passwd="mni123#@!",
        database="stocks"
    )
    mycursor = mydb.cursor()

    # set driver parameters
    run_driver = driver()
    url = "https://www.bursamalaysia.com/market_information/shariah_compliant_equities_prices?per_page=50"
    open_url = run_driver.get(url)

    page = 1
    while True:
        # stop if reach max page
        if page == max_page():
            log.info(f"all {max_page()} collected")
            break
        else:
            # scrap web page
            log.info(max_page())

            current_url = run_driver.current_url
            new_url = run_driver.get(f"{url}&page={page}")
            scrap_page = (data('odd') + data('even'))

            for scrap_rows in scrap_page:
                # clean data
                clean_rows = scrap_rows.replace("\n", " ").replace("\"", "").replace(",", "")\
                                       .replace("[", "").replace("]", "").replace("+", "")
                each_row = clean_rows.split()
                if len(each_row) == 18:
                    del each_row[4]
                elif len(each_row) == 16:
                    each_row.insert(4, "-")
                elif len(each_row) == 15:
                    each_row.insert(4, "-")
                    each_row.insert(4, "-")
                each_row.extend([current_time(),current_time(),current_epoch()])
                print(each_row)

                # sql transfer row by row
                sql_string = """INSERT INTO stocks.stocks_raw
                            (no,name,syariah,code,dividend_type,rem,last_done,lacp,chg,
                            chg_percentage,volume,buy_volume,buy,sell,sell_volume,high,low,
                            time_created,time_updated,time_epoch)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                mycursor.execute(sql_string, each_row)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")

            page += 1
            sleep(.5)
        continue

    run_driver.close()
    t1 = time()
    timer = t1 - t0
    print(timer)
