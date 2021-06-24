"""
	This module defines the config class that contains all the settings
	used in the other modules
"""
from dataclasses import dataclass
# default parameters for the config
URL_BASE = "https://services.datasport.com/"
URL_END = "/lauf/zuerich/alfab.htm"
YEARS_LIST = list(range(2014, 2019))
AGE_GROUPS = [[0, 20], [21, 30], [31, 40], [41, 50], [51, 110]]


# WARNING: if changes are made to field_nmaes, field types and field orders should be changed as well
FIELD_NAMES = ["Id", "Category", "Rang", "Fullname", "Age_year", "Location", "total_time", "Run_link", "Run_year"]
FIELD_TYPES = ["integer primary key autoincrement", "varchar", "varchar", "varchar", "integer", "varchar", "timestamp", "varchar", "integer" ]
# FIELD ORDER refers to the order in the webpage, and should be changed accordingly
FIELD_ORDERS = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# Below the sql types from sqlalchemy library, needed for populating the database from pandas
DB_FILE_PATH = "assets/runners_db.sqlite"


@dataclass
class ConfigClass:
    url_base: str = None
    url_end: str = None
    years: list = None
    age_groups: list = None
    field_names: list = None
    field_types: list = None
    field_orders: list = None
    db_file_path: str = None


# create config object with default variables
config = ConfigClass(URL_BASE, URL_END, YEARS_LIST, AGE_GROUPS, FIELD_NAMES, FIELD_TYPES, FIELD_ORDERS, DB_FILE_PATH)

if __name__ == "__main__":
    print(config)
