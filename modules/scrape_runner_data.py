"""
    This module scrapes runner data from the web and returns
     it as dataframe
"""
import os
import re
from pandas import DataFrame, concat
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
    runner_data = soup.findAll("font", {"size": "2"})
    return list(runner_data)


def prepare_str(single_runner_data, delimiter="#") -> list:
    """prepares string for attribute extraction cleaning the string and splitting it into a list of string """
    clean_str = re.sub(r" {2,}", delimiter, single_runner_data)
    clean_str = re.sub("(?<=[0-9])(\s)(?=[A-Z\u00C0-\u00FF])", delimiter, clean_str)
    clean_str = re.sub("(?<=[a-z\u00C0-\u00FF])(\s)(?=[0-9])", delimiter, clean_str)
    clean_str = re.sub("(?<=[0-9])(\. )(?=[A-Z\u00C0-\u00FF])", delimiter, clean_str)
    return clean_str.split(delimiter)


def get_run_link(single_runner_data) -> str:
    try:
        return single_runner_data.find("a", href=True)["href"]
    except TypeError:
        return "missing link"


def create_runner_df(runner_data, field_names, year) -> dict:
    """sets attributes and builds a dataframe"""
    runner_data_list = []
    for single_runner_data in runner_data[2:-1]:

        single_runner_list = prepare_str(single_runner_data.text)
        if len(single_runner_list) >= 6:
            single_runner_dict = {field_names[1]: single_runner_list[0],
                                  field_names[2]: single_runner_list[1],
                                  field_names[3]: single_runner_list[2],
                                  field_names[4]: single_runner_list[3],
                                  field_names[5]: single_runner_list[4],
                                  field_names[6]: single_runner_list[5],
                                  field_names[7]: get_run_link(single_runner_data),
                                  field_names[8]: year,
                                  }
            runner_data_list.append(single_runner_dict)
    return DataFrame(runner_data_list)


def scrape_single_year(url, year, field_names) -> DataFrame:
    """scrapes all the runner data, extracts the attributes and """
    html_content = get_runner_data(url)
    runner_data = parse_runner_data(html_content)
    runner_data_df = create_runner_df(runner_data, field_names, year)
    return runner_data_df


def main(config) -> DataFrame:
    """scrapes data about runners adn returns a dataframe"""
    year_df_list = []
    for year in config.years:
        url = create_url(config.url_base, year, config.url_end)
        year_df = scrape_single_year(url, year, config.field_names)
        year_df_list.append(year_df)
    return concat(year_df_list)

if __name__ == "__main__":
    os.chdir("..")
    from config import config

    url = create_url(config.url_base, config.years[0], config.url_end)
    print("first url is:", url)
    html_content = get_runner_data(url)
    runner_data = parse_runner_data(html_content)
    link = runner_data[2:][0].find_all("a", href=True)[0]["href"]
    print(link)
    my_df = create_runner_df(runner_data, config.field_names, config.years[0])
    complete_runner_df = main(config)
    print(complete_runner_df)

