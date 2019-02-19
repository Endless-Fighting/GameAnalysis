#-*-coding:utf-8-*

import json
from urllib import request

import time

# the api_key string will be expired 24 hours after applying each time, so it need updating mostly every time
api_key = "RGAPI-20aaff70-57b7-44b1-b66e-9cbbef7c8865"
# the account id of the top one player in the north America, used as the seed account
seed_account_id = "37281196"


def get_match_ids_by_account_id(account_id):
    """
    get the match ids that the player with the account id participated using the API
    :param account_id:
    :return: match id list
    """
    match_ids = []

    time.sleep(0.5) # the API used below has rate limits

    try:
        url="https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/" + str(account_id) + "?season=11&api_key=" + api_key
        req = request.Request(url)
        res = request.urlopen(req)
        matches = json.loads(res.read())['matches']

        for match in matches:
            match_ids.append(match['gameId'])
    except Exception as e:
        print("wrong in get_match_ids_by_account_id, check whether the api_key is expired")
        print(e)
        return None

    return match_ids


def get_champion_match_data_list_and_account_ids_by_match_id(match_id):
    """
    get the match data and the account ids of the participants in the match with the match id
    :param match_id:
    :return: champion match data list, account id list
    """
    champion_match_data_list = []
    account_ids = []

    time.sleep(0.5) # the API used below has rate limits

    try:
        url = "https://na1.api.riotgames.com/lol/match/v3/matches/" + str(match_id) + "?api_key=" + api_key
        req = request.Request(url)
        res = request.urlopen(req)
        result_dict = json.loads(res.read())

        for participant in result_dict['participants']:
            champion_match_data = [match_id, participant['championId']]
            stats = participant['stats']
            champion_match_data.append(stats['kills'])
            champion_match_data.append(stats['deaths'])
            champion_match_data.append(stats['assists'])
            champion_match_data.append(stats['totalDamageDealtToChampions'])
            champion_match_data.append(stats['magicDamageDealtToChampions'])
            champion_match_data.append(stats['physicalDamageDealtToChampions'])
            champion_match_data.append(stats['trueDamageDealtToChampions'])
            champion_match_data.append(stats['totalHeal'])
            champion_match_data.append(stats['totalDamageTaken'])
            champion_match_data_list.append(champion_match_data)

        for participant in result_dict['participantIdentities']:
            account_ids.append(participant['player']['accountId'])
    except Exception as e:
        print("wrong in get_champion_match_data_list_and_account_ids_by_game_id, check whether the api_key is expired")
        print(e)
        return None, None

    return champion_match_data_list, account_ids


if __name__ == '__main__':
    print(get_match_ids_by_account_id(37281196))