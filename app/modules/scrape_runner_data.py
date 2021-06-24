"""
    This module scrapes runner data from the web and returns
     it as dataframe
"""
import os
import re
from pandas import DataFrame, concat
import requests
from bs4 import BeautifulSoup
import sys
sys.path.append("..")
from classes import Runner, Marathon

def create_url(base, year, end) -> str:
    """creates the url to parse for different years"""
    return base + str(year) + end


def get_runner_data(url):
    """parses webpage using requests and returns the html content"""
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError
    else:
        return response


def parse_runner_data(html_content, tag="font", attrs = {"size": "2"}) -> list:
    """parses html content for relevant data"""
    soup = BeautifulSoup(html_content.text, "html.parser")
    runner_data = soup.findAll(tag, attrs)
    return list(runner_data)

def get_run_link(single_runner_data) -> str:
    try:
        return single_runner_data.find("a", href=True)["href"]
    except TypeError:
        return "missing link"

def prepare_str(single_runner_data, delimiter="##") -> list:
    """prepares string for attribute extraction cleaning the string and splitting it into a list of string """
    clean_str = single_runner_data
    clean_str = re.sub(r" {2,}", delimiter, clean_str)
    clean_str = re.sub("(?<=[0-9])(\s)(?=[a-zA-Z\u00C0-\u00FF])", delimiter, clean_str)
    clean_str = re.sub("(?<=[A-Za-z\u00C0-\u00FF\.])(\s)(?=[0-9])", delimiter, clean_str)
    clean_str = re.sub("(?<=[0-9])(\.\s)(?=[a-zA-Z\u00C0-\u00FF])", delimiter, clean_str)
    clean_str = re.sub("(?<=[0-9])(\.\s)(?=[a-zA-Z\u00C0-\u00FF])", delimiter, clean_str)
    single_runner_list = clean_str.split(delimiter)[:6]
    return single_runner_list



#Deprecated
# def create_runner_df(runner_data, field_names, year) -> DataFrame:
#     """sets attributes and builds a dataframe"""
#     runner_data_list = []
#     for single_runner_data in runner_data[2:-1]:
#
#         single_runner_list = prepare_str(single_runner_data.text)
#         if len(single_runner_list) >= 6:
#             single_runner_dict = {field_names[1]: single_runner_list[0],
#                                   field_names[2]: single_runner_list[1],
#                                   field_names[3]: single_runner_list[2],
#                                   field_names[4]: single_runner_list[3],
#                                   field_names[5]: single_runner_list[4],
#                                   field_names[6]: single_runner_list[5],
#                                   field_names[7]: get_run_link(single_runner_data),
#                                   field_names[8]: year,
#                                   }
#             runner_data_list.append(single_runner_dict)
#     return DataFrame(runner_data_list)
#
#
# def scrape_single_year(url, year, field_names) -> DataFrame:
#     """scrapes all the runner data, extracts the attributes and """
#     html_content = get_runner_data(url)
#     runner_data = parse_runner_data(html_content)[2:-1]
#     runner_data_df = create_runner_df(runner_data, field_names, year)
#     return runner_data_df


def main(config) -> [Marathon]:
    """scrapes data about runners for all years and returns a dataframe"""
    marathon_list = []
    for year in config.years:
        url = create_url(config.url_base, year, config.url_end)
        html_content = get_runner_data(url)
        runner_data = parse_runner_data(html_content)[2:-1]

        # create list of runner objects
        runner_list=[]
        for n,single_runner_data in enumerate(runner_data):
            single_runner_attrs = prepare_str(single_runner_data.text)
            if len(single_runner_attrs) == 6:
                single_runner_attrs.insert(0, str(n)) # adds ID
                single_runner_attrs.insert(7, get_run_link(single_runner_data))  # adds link
                single_runner_attrs.insert(8, year) # adds year
                runner = Runner(config, single_runner_attrs)
                runner_list.append(runner)
        marathon= Marathon(year, runner_list)
        marathon_list.append(marathon)
    return marathon_list

if __name__ == "__main__":
    import os
    import sys

    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
    print(sys.path)

    # import sys
    # sys.path.append("..")
    from config import config
    #
    my_marathon_list = main(config)
    print(my_marathon_list)

