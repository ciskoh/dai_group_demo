"""
    This module creates the database and populates it with
    data retrieved by scrape_runner_data
"""

import sys

sys.path.append("..")
import sqlite3
from sqlite3 import Error, Connection

from config import config
from modules import scrape_runner_data


def create_sqlite_db(db_file_path) -> Connection:
    """initializes a sqlite instance"""
    conn = None
    try:
        conn = sqlite3.connect(db_file_path)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            return conn

def populate_db(conn, runner_data_df):
    """inserts scraped_data in the sqlite database"""
    runner_data_df.to_sql('runners', conn)

#TODO: add checks
def check_df(df):
    """check that data was inserted correctly"""
    for n in range(len(df["Age_year"])):
        if not df["Age_year"].iloc[[n]].values[0].isdecimal():
            print("problem here", df.iloc[[n]].values)
            raise ValueError



def main(config) -> None:
    """main function that creates db and populates it """

    conn = create_sqlite_db(config.db_file_path)

    runner_data_df = scrape_runner_data(config)
    check_df(runner_data_df)
    populate_db(conn, runner_data_df)


    conn.close
    return None

if __name__ == "__main__":
    import os

    os.chdir("..")

    main(config)