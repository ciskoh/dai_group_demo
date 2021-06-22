"""
    This module creates the database and populates it with
    data retrieved by scrape_runner_data
"""

import sys

sys.path.append("..")
import sqlite3
from sqlite3 import Error, Connection
from pandas import to_datetime, to_numeric
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

def check_df(df, field_types):
    """converts data type for each column of the dataFrame according to field_types
    and throws an error if not possible"""
    for n in range(len(df.columns)):
        if field_types[n]=="varchar":
            try:
                df[df.columns[n]]=df[df.columns[n]].astype('str')
            except ValueError:
                raise ValueError(f"column {df.columns[n]} is not a {field_types[n]} ")
    if ( field_types[n] == "integer") or ("integer" in field_types.split(" ")):
        try:
            df[df.columns[n]] = df[df.columns[n]].astype('int')
        except ValueError:
            raise ValueError(f"column {df.columns[n]} is not a {field_types[n]}")
    if field_types[n] == "timestamp":
        try:
            df[df.columns[n]] = to_datetime(df[df.columns[n]], errors='coerce')
        except ValueError:
            raise ValueError(f"column {df.columns[n]} is not a {field_types[n]}")
    return df

def create_table_definition(table_name, field_names, fields_definitions, ) -> str:
    """ generates string for sql table creation
    :param  field_names: field names
   :param  field_names: field names
   :param field_definitions: field type
   :return: str
   """
    field_list = zip(field_names, fields_definitions)
    sql_table_def = ""
    for i in field_list:
        sql_table_def += f"{i[0]} {i[1].upper()},\n"
    sql_complete_str = f" CREATE TABLE IF NOT EXISTS {table_name} ( {sql_table_def[:-2]} ); "
    return sql_complete_str

def populate_db(conn, runner_data_df, field_names, field_types2):
    """inserts scraped_data in the sqlite database"""
    field_types_dict = dict(zip(field_names,field_types2))
    runner_data_df.to_sql('runners', conn, dtype=field_types_dict )




def main(config) -> None:
    """main function that creates db and populates it """
    conn = create_sqlite_db(config.db_file_path)
    runner_data_df = scrape_runner_data(config)
    runner_data_df = check_df(runner_data_df, config.field_types)
    populate_db(conn, runner_data_df, config.field_names, config.field_types)

    conn.close
    return None

if __name__ == "__main__":
    import os

    os.chdir("..")

    main(config)