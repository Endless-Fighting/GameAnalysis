#-*-coding:utf-8-*

import  utils.DataCollector as dc
import  utils.SQLiteUtils as sqlite
import json
import numpy


def champion_match_data_getter():
    """
    try to get the match data of a single match and store in database
    :return:  true if getting match data successfully, otherwise false
    """
    match_id = sqlite.get_next_match_id()
    if match_id is None:
        return False
    champion_match_data_list, account_ids = dc.get_champion_match_data_list_and_account_ids_by_match_id(match_id)
    if champion_match_data_list is None:
        return False
    for champion_match_data in champion_match_data_list:
        sqlite.insert_champion_match_data(champion_match_data)
    for account_id in account_ids:
        sqlite.insert_account_id(account_id)
    sqlite.set_match_id(match_id)
    return True


def match_id_getter():
    """
    try to get match id participated by a single account and store in database
    :return: true if getting match id successfully, otherwise false
    """
    account_id = sqlite.get_next_account_id()
    if account_id is None:
        return False
    match_ids = dc.get_match_ids_by_account_id(account_id)
    if match_ids is None:
        sqlite.delete_account_id(account_id)
        return False
    for match_id in match_ids:
        sqlite.insert_match_id(match_id)
    sqlite.set_account_id(account_id)
    return True


def fill_match_ids(count):
    """
    load count match id into database for processing and analysing
    :param count:
    :return:
    """
    while sqlite.get_table_count("match") < count:
        while(match_id_getter()):
            pass
        champion_match_data_getter()


def fill_match_data():
    """
    load all the match data for match id in the database
    :return:
    """
    while champion_match_data_getter():
        pass


def champion_info_getter():
    """
    load static json champion info into database
    :return:
    """
    champion_info_file = open(r"../data/champion.json", encoding='utf-8')
    result_dict = json.load(champion_info_file)
    data = result_dict['data']
    for key in data:
        champion_info = data[key]
        sqlite.insert_champion_info(int(champion_info['key']), champion_info['id'], champion_info['name'], champion_info['title'])
    return


def compute_average_champion_data():
    """
    compute the typical value for each champion
    :return:
    """
    for champion_id in sqlite.get_champion_info_dict():
        match_data_list = sqlite.get_champion_match_data(champion_id)
        print("champion with championId " + str(champion_id) + " has " + str(len(match_data_list)) + " match records" )
        sum_list = numpy.sum(match_data_list, axis=0)
        avg_list = [int(i/len(match_data_list)) for i in sum_list]
        sqlite.insert_champion_data([champion_id] + avg_list)
    return


if __name__ == '__main__':
    # first step: load static json champion info into database
    champion_info_getter()

    # second step: get enough match data using API
    fill_match_ids(15000)
    fill_match_data()

    # last step: compute the typical value for each champion after data cleaning
    sqlite.data_cleaning()
    compute_average_champion_data()
