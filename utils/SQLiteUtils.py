#-*-coding:utf-8-*

import sqlite3


def get_connect():
    """
    get the connection of the database, should be used by each database method
    :return: the connection of the database
    """
    conn = sqlite3.connect(r"../data/info.db")

    # print("connect successfully")
    #
    # conn.execute('''CREATE TABLE IF NOT EXISTS account
    #        (accountId INT PRIMARY KEY NOT NULL,
    #        isSearched BOOLEAN NOT NULL);''')
    # print("create account successfully")
    #
    # conn.execute('''CREATE TABLE IF NOT EXISTS match
    #            (matchId INT PRIMARY KEY NOT NULL,
    #            isSearched BOOLEAN NOT NULL);''')
    # print("create match successfully")
    #
    # conn.execute('''CREATE TABLE IF NOT EXISTS championMatchData
    #            (matchId INT NOT NULL,
    #            championId INT NOT NULL,
    #            kills INT NOT NULL,
    #            deaths INT NOT NULL,
    #            assists INT NOT NULL,
    #            totalDamage INT NOT NULL,
    #            magicDamage INT NOT NULL,
    #            physicalDamage INT NOT NULL,
    #            trueDamage INT NOT NULL,
    #            totalHeal INT NOT NULL,
    #            totalDamageTaken INT NOT NULL,
    #            PRIMARY KEY (matchId,championId));''')
    # print("create championMatchData successfully")
    #
    # conn.execute('''CREATE TABLE IF NOT EXISTS championData
    #                (championId INT PRIMARY KEY NOT NULL,
    #                kills INT NOT NULL,
    #                deaths INT NOT NULL,
    #                assists INT NOT NULL,
    #                totalDamage INT NOT NULL,
    #                magicDamage INT NOT NULL,
    #                physicalDamage INT NOT NULL,
    #                trueDamage INT NOT NULL,
    #                totalHeal INT NOT NULL,
    #                totalDamageTaken INT NOT NULL);''')
    # print("create championData successfully")
    #
    # conn.execute('''CREATE TABLE IF NOT EXISTS championInfo
    #            (championId INT PRIMARY KEY NOT NULL,
    #            key TEXT NOT NULL,
    #            name TEXT NOT NULL,
    #            title TEXT NOT NULL);''')
    # print("create championInfo successfully")
    return conn


def insert_account_id(account_id):
    """
    if not exist the same account_id, then insert it to table account, and set mark search with false
    :param account_id:
    :return:
    """
    conn = get_connect()
    cursor = conn.execute("SELECT * FROM account where accountId = ?", [account_id])
    result_list = cursor.fetchall()
    if len(result_list) == 0:
        conn.execute("INSERT INTO account \
                  VALUES (?, 0)", [account_id])
        print("accountId " + str(account_id) + " is inserted")
    else:
        print("accountId " + str(account_id) + " already exists!")
    conn.commit()
    conn.close()
    return


def insert_match_id(match_id):
    """
    if not exist the same match_id, then insert it to table match, and set mark search with false
    :param match_id:
    :return:
    """
    conn = get_connect()
    cursor = conn.execute("SELECT * FROM match where matchId = ?", [match_id])
    result_list = cursor.fetchall()
    if len(result_list) == 0:
        conn.execute("INSERT INTO match \
                      VALUES (?, 0)", [match_id])
        print("matchId " + str(match_id) + " is inserted")
    else:
        print("matchId " + str(match_id) + " already exists!")
    conn.commit()
    conn.close()
    return


def insert_champion_match_data(champion_match_data):
    """
    if not exist the same champion_match_data, then insert it to table championMatchData
    :param champion_match_data:
    :return:
    """
    conn = get_connect()
    cursor = conn.execute("SELECT * FROM championMatchData where matchId = ? AND championId = ?",
                          [champion_match_data[0], champion_match_data[1]])
    result_list = cursor.fetchall()
    if len(result_list) == 0:
        conn.execute("INSERT INTO championMatchData \
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", champion_match_data)
        print("champion_match_data (" + str(champion_match_data[0]) + "," + str(champion_match_data[1]) + ") is inserted")
    else:
        print("champion_match_data " + str(champion_match_data[0]) + "," + str(champion_match_data[1]) + " already exists!")
    conn.commit()
    conn.close()
    return


def insert_champion_data(champion_data):
    """
    insert the champion_data to table championData
    :param champion_data:
    :return:
    """
    conn = get_connect()
    conn.execute("DELETE FROM championData WHERE championId = " + str(champion_data[0]))
    conn.execute("INSERT INTO championData \
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", champion_data)
    conn.commit()
    conn.close()
    print("champion_data " + str(champion_data[0]) + " is inserted")
    return


def get_next_match_id():
    """
    get the next match id to be searched from table match
    :return: match id to be searched or None if there is no more matchId to be searched
    """
    conn = get_connect()
    cursor = conn.execute("SELECT matchId FROM match WHERE isSearched = 0 LIMIT 1")
    result_list = cursor.fetchone()
    conn.close()
    if result_list is None:
        print("no more matchId to be searched")
        return None
    else:
        match_id = result_list[0]
        return match_id


def get_next_account_id():
    """
    get the next account id to be searched from table account
    :return: account id to be searched or None if there is no more account to be searched
    """
    conn = get_connect()
    cursor = conn.execute("SELECT accountId FROM account WHERE isSearched = 0 LIMIT 1")
    result_list = cursor.fetchone()
    conn.close()
    if result_list is None:
        print("no more accountId to be searched")
        return None
    else:
        account_id = result_list[0]
        return account_id


def get_table_count(table_name):
    """
    get the count of the records in the corresponding table
    :param table_name:
    :return:
    """
    conn = get_connect()
    cursor = conn.execute("SELECT COUNT(*) FROM " + table_name)
    count = cursor.fetchall()[0][0]
    conn.close()
    return count


def set_match_id(match_id):
    """
    mark the matchId with isSearched true
    :param match_id:
    :return:
    """
    conn = get_connect()
    conn.execute("UPDATE match SET isSearched = 1 WHERE matchId = " + str(match_id))
    conn.commit()
    conn.close()
    print("matchId " + str(match_id) + " has been searched")
    return


def delete_account_id(account_id):
    """
    sometimes the account id is invalid to get match data from the API, used to delete the invalid account id
    :param account_id:
    :return:
    """
    conn = get_connect()
    conn.execute("DELETE from account WHERE accountId = ?", [account_id])
    conn.commit()
    conn.close()
    return



def set_account_id(account_id):
    """
    mark the accountId with isSearched true
    :param account_id:
    :return:
    """
    conn = get_connect()
    conn.execute("UPDATE account SET isSearched = 1 WHERE accountId = " + str(account_id))
    conn.commit()
    conn.close()
    print("accountId " + str(account_id) + " has been searched")
    return


def get_champion_match_data(champion_id):
    """
    get the match data list with corresponding champion id
    :param champion_id:
    :return: match data list with corresponding champion id
    """
    conn = get_connect()
    cursor = conn.execute("SELECT * FROM championMatchData WHERE championId = ? ",[champion_id])
    result_list = []
    for row in cursor:
        result_list.append(row[2:])
    conn.close()
    return result_list


def insert_champion_info(champion_id, key, name, title):
    """
    insert the champion info into table championInfo
    :param champion_id:
    :param key:
    :param name:
    :param title:
    :return:
    """
    conn = get_connect()
    cursor = conn.execute("SELECT * FROM championInfo where championId = ?", [champion_id])
    result_list = cursor.fetchall()
    if len(result_list) == 0:
        conn.execute("INSERT INTO championInfo \
                          VALUES (?, ?, ?, ?)", [champion_id, key, name, title])
        print("championInfo of " + str(champion_id) + " is inserted")
    else:
        print("championInfo of " + str(champion_id) + " already exists!")
    conn.commit()
    conn.close()
    return


def get_champion_info_dict():
    """
    get the champion info dictionary with champion id being key
    :return: champion info dictionary
    """
    conn = get_connect()
    cursor = conn.execute("SELECT * FROM championInfo ORDER BY championId")
    info_dict = {}
    for row in cursor:
        info_dict[row[0]] = [row[1], row[2], row[3]]
    conn.close()
    return info_dict


def get_standardized_champion_data():
    """
    get the standardized champion data using extreme value normalization method
    :return: standardized champion data list
    """
    conn = get_connect()
    columns = ["kills", "deaths", "assists", "totalDamage", "magicDamage",
               "physicalDamage", "trueDamage", "totalHeal", "totalDamageTaken"]
    max_list = [0]
    min_list = [0]
    for column in columns:
        cursor = conn.execute("SELECT MAX(" + column + ") FROM championData")
        max_list.append(cursor.fetchone()[0])
        cursor = conn.execute("SELECT MIN(" + column + ") FROM championData")
        min_list.append(cursor.fetchone()[0])
    #print(max_list)
    #print(min_list)

    standardized_champion_data = []
    cursor = conn.execute("SELECT * FROM championData ORDER BY championId")
    for row in cursor:
        single_champion_data = []
        for i in range(1,10):
            single_champion_data.append( (row[i]-min_list[i]) / (max_list[i]-min_list[i]) )
        standardized_champion_data.append(single_champion_data)

    conn.close()
    return standardized_champion_data


def data_cleaning():
    """
    remove the seemingly invalid match data from the table championMatchData
    :return:
    """
    conn = get_connect()
    conn.execute("DELETE FROM championMatchData WHERE kills < 2 AND deaths < 2 AND assists < 2")
    conn.commit()
    conn.close()
    return


def clear_data():
    """
    clear the data in the database, used for debugging
    :return:
    """
    conn = get_connect()
    #conn.execute("DELETE from match")
    #conn.execute("DELETE from account")
    #conn.execute("DELETE from championMatchData")
    conn.execute("DELETE from championData")
    conn.commit()
    conn.close()
    print("all data in info.db has been cleared")
    return


if __name__ == '__main__':
    #clear_data()
    print("the count of table championInfo: " + str(get_table_count("championInfo")))
    print("the count of table match: " + str(get_table_count("match")))
    print("the count of table account: " + str(get_table_count("account")))
    print("the count of table championMatchData: " + str(get_table_count("championMatchData")))
    print("the count of table championData: " + str(get_table_count("championData")))

    #print(get_standardized_champion_data())
    #print(get_champion_match_data(1))

