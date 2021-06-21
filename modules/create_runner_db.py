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

# DEPRECATED
# def create_table_definition(table_name, field_names, field_defs ) -> str:
#     """ generates string for sql table creation
#     :param  table_name: name of the table to be created
#    :param  field_names: field names
#    :param field_definitions: field type
#    :return: str
#    """
#     field_list = zip(field_names, field_defs)
#     sql_table_def = ""
#     for i in field_list:
#         sql_table_def += f"{i[0]} {i[1].upper()},\n"
#     sql_complete_str = f" CREATE TABLE IF NOT EXISTS {table_name} ( {sql_table_def[:-2]} ); "
#     return sql_complete_str

# DEPRECATED
# def create_table(conn, sql_table_definition) -> None:
#     """ create a table from the table_sql statement
#        :param conn: Connection object
#        :param table_sql: a CREATE TABLE statement
#        :return: None
#        """
#     try:
#         c = conn.cursor()
#         c.execute(sql_table_definition)
#     except Error as e:
#         print(e)


def populate_db(conn, runner_data_df):
    """inserts scraped_data in the sqlite database"""
    runner_data_df.to_sql('runners', conn)


def check_db(db):
    """check that data was inserted correctly"""
    return NotImplementedError()


def main(config) -> None:
    """main function that creates db and populates it """

    conn = create_sqlite_db(config.db_file_path)

    runner_data_df = scrape_runner_data(config)
    populate_db(conn, runner_data_df)

    check_db(conn)
    return None

if __name__ == "__main__":
    import os

    os.chdir("..")

    main(config)