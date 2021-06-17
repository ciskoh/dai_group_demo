"""
    This module scrapes runner data from the web and returns
     it as dataframe
"""
import os
import re
from pandas import DataFrame
import requests
from bs4 import BeautifulSoup


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


def parse_runner_data(html_content) -> list:
    """parses html content for relevant data"""
    soup = BeautifulSoup(html_content.text, "html.parser")
    runner_data = soup.findAll("font", {"size" : "2"})
    return list(runner_data[2:])

# these functions extract 1 field each corresponding to desired database attributes
def extract_runner_attr1(single_runner_data) -> str:
    """returns category"""
    return single_runner_data.text.split(" ")[0]

def extract_runner_attr2(single_runner_data) -> str:
    """returns Rang"""
    #TODO: continue from here
def extract_runner_attr3(single_runner_data) -> str:
    return NotImplementedError
def extract_runner_attr4(single_runner_data) -> str:
    return NotImplementedError

def extract_runner_attr5(single_runner_data) -> str:
    return NotImplementedError

def extract_runner_attr6(single_runner_data) -> str:
    return NotImplementedError

def extract_runner_attr7(single_runner_data) -> str:
    return NotImplementedError

def extract_runner_attr8(single_runner_data) -> str:
    return NotImplementedError

def extract_runner_attr9(single_runner_data) -> str:
    return NotImplementedError


def extract_runner_data(runner_data, field_names) -> dict:
    """sets correct datatype and builds a dataframe"""
    runner_list = []
    for single_runner_data in runner_data:
    single_runner_dict = { field_names[1]: extract_runner_attr1(single_runner_data),
                           field_names[2]: extract_runner_attr2(single_runner_data),
                           field_names[3]: extract_runner_attr3(single_runner_data),
                           field_names[4]: extract_runner_attr4(single_runner_data),
                           field_names[5]: extract_runner_attr5(single_runner_data),
                           field_names[6]: extract_runner_attr6(single_runner_data),
                           field_names[7]: extract_runner_attr7(single_runner_data),
                           field_names[8]: extract_runner_attr8(single_runner_data),
                           field_names[9]: extract_runner_attr9(single_runner_data),
                           }
    """ extract each desired attribute for eahc runner and returns a dict"""

def main(config) -> DataFrame:
    """main function that scrapes all the runner data"""
    url = create_url(config.base, config.year, config.end)
    html_content = get_runner_data(url)
    runner_data = parse_runner_data(html_content)
    runner_data_df = reshape_runner_data(runner_data)
    return runner_data_df


if __name__ == "__main__":
    os.chdir("..")
    from config import config

    url = create_url(config.url_base, config.years[0], config.url_end)
    print("first url is:", url)
    html_content = get_runner_data(url)
    runner_data = parse_runner_data(html_content)
    str_fields = parse_str_fields(runner_data[0])
    print(str_fields)
