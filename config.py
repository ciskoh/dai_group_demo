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

# WARNING: changing field names and defs will not work unless function \
# create_runner_df in scrape_runner_data is updated too!
FIELD_NAMES = ["Id", "Category", "Rang", "Fullname", "Age_year", "Location", "total_time", "run_link", "run_year"]
FIELD_DEFS = ["integer primary key autoincrement", "varchar", "varchar", "varchar", "integer", "varchar", "timestamp",
              "varchar", "integer"]
DB_FILE_PATH = "assets/runners_db.db"


@dataclass
class ConfigClass:
    url_base: str = None
    url_end: str = None
    years: list = None
    age_groups: list = None
    field_names: list = None
    field_defs: list = None
    db_file_path: str = None


# create config object with default variables
config = ConfigClass(URL_BASE, URL_END, YEARS_LIST, AGE_GROUPS, FIELD_NAMES, FIELD_DEFS, DB_FILE_PATH)

if __name__ == "__main__":
    print(config)
