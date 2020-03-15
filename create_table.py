# -*- coding: utf-8 -*-

"""
To create database and tables for stocks
"""

__author__ = 'MNI'
__version__ = '1.0'

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="nafizizzat",
    passwd="mni123#@!",
    database="stocks"
)

# create database if does not exist
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS stocks;")

# create table if does not exist
mycursor.execute("SHOW TABLES")
print([x for x in mycursor])

mycursor.execute("""CREATE TABLE stocks_raw (id INT AUTO_INCREMENT PRIMARY KEY
                                            ,no float
                                            ,name VARCHAR(255)
                                            ,syariah VARCHAR(255)
                                            ,code VARCHAR(255)
                                            ,dividend_type VARCHAR(255)
                                            ,rem VARCHAR(255)
                                            ,last_done VARCHAR(255)
                                            ,lacp VARCHAR(255)
                                            ,chg VARCHAR(255)
                                            ,chg_percentage VARCHAR(255)
                                            ,volume VARCHAR(255)
                                            ,buy_volume VARCHAR(255)
                                            ,buy VARCHAR(255)
                                            ,sell VARCHAR(255)
                                            ,sell_volume VARCHAR(255)
                                            ,high VARCHAR(255)
                                            ,low VARCHAR(255)
                                            ,time_created date
                                            ,time_updated date
                                            ,time_epoch VARCHAR(255))"""
                 )
print([x for x in mycursor])