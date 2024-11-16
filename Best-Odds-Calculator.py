from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import difflib
import re


# Splits a list into separate elements if there are newlines.
def split_list_by_newline(lst):
    result = []
    for item in lst:
        if '\n' in item:
            result.extend(item.split('\n'))
        else:
            result.append(item)
    return result


# Replaces commas with periods in a given text.
def replace_comma_with_period(text):
    return text.replace(",", ".")


# Removes the "vs" part from a given text.
def remove_vs(text):
    return text.replace("\nvs", "")


# Finds the index of the first non-tuple element in the list.
def find_first_non_tuple_index(lst):
    for index, element in enumerate(lst):
        if not isinstance(element, tuple):
            return index
    return len(lst) + 2


# Strips empty or whitespace-only elements from the list.
def remove_empty_elements(lst):
    return [item for item in lst if item.strip()]


# Finds the closest match to the given word from a list of words.
def find_closest_match(word, lst):
    return difflib.get_close_matches(word, lst, cutoff=0)[0]


# Swaps elements in each list based on their closeness to the reference list.
def align_lists_by_closeness(lists, lists2, n):
    reference_list = lists[0]
    
    for index, word in enumerate(reference_list):
        for j in range(1, n):
            closest_match = find_closest_match(word, lists[j])
            closest_match_index = lists[j].index(closest_match)
            lists[j][index], lists[j][closest_match_index] = lists[j][closest_match_index], lists[j][index]
            lists2[j][index], lists2[j][closest_match_index] = lists2[j][closest_match_index], lists2[j][index]

    return lists, lists2


# Finds the minimum number of teams across all data lists.
def find_min_teams(data, n):
    min_teams = len(data[0]["teams"])
    for i in range(n):
        if len(data[i]["teams"]) < min_teams:
            min_teams = len(data[i]["teams"])
    return min_teams


# Scrapes odds and teams data from multiple websites.
def get_ligue1_odds(site_urls, container_classes, match_classes, odds_classes, M=0, N=9999):
    options = Options()
    options.add_argument('--disable-gpu')
    options.headless = True  # Run browser in headless mode
    service = Service("C:\\Python\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    
    all_data = []
    
    for url, container_class, match_class, odds_class in zip(site_urls, container_classes, match_classes, odds_classes):
        driver.get(url)
        time.sleep(5)
        
        containers = driver.find_elements(By.CLASS_NAME, container_class)    
        site_data = {'teams': [], 'odds': []}
        
        for container in containers:
            i, j = 1, 2
            team_elements = container.find_elements(By.CLASS_NAME, match_class)
            teams = [remove_vs(i.text.strip()) for i in team_elements]
            teams = split_list_by_newline(teams)
            
            while i < len(teams):
                teams[i-1] += " vs " + teams[i]
                del teams[i]
                i += 1
            
            odd_elements = container.find_elements(By.CLASS_NAME, odds_class)
            odds = [replace_comma_with_period(i.text.strip()) for i in odd_elements]
            odds = remove_empty_elements(odds)
            
            if not odds:
                for element in odd_elements:
                    raw_text = element.get_attribute("innerHTML")
                    match_odds = re.search(r'\d+,\d+', raw_text)
                    if match_odds:
                        odd_value = match_odds.group(0)
                        odd_value = replace_comma_with_period(odd_value)
                        if 1.01 < float(odd_value) < 20:
                            odds.append(odd_value)
            
            while j < len(odds) and j <= len(teams) + 1:
                odds[j] = (odds[j-2], odds[j-1], odds[j])
                del odds[j-1]
                del odds[j-2]
                j += 1

            odds = odds[:find_first_non_tuple_index(odds)]
            N = abs(len(teams) - N)
            teams, odds = teams[M:N], odds[M:N]
            site_data['teams'].extend(teams)
            site_data['odds'].extend(odds)
        
        all_data.append(site_data)
    
    driver.quit()
    
    min_teams = find_min_teams(all_data, len(site_urls))
    y = all_data[0]["teams"][:min_teams]
    L1 = [all_data[i]["teams"][:min_teams] for i in range(len(site_urls))]
    L2 = [all_data[i]["odds"][:min_teams] for i in range(len(site_urls))]
    
    aligned_data = align_lists_by_closeness(L1, L2, len(site_urls))
    
    for i in range(len(site_urls)):
        all_data[i]["teams"], all_data[i]["odds"] = y, aligned_data[1][i]
        print(all_data[i]["teams"])
        print(all_data[i]["odds"])
    
    print("")
    return all_data


# Example usage with URLs for different leagues
site_urls = [
    ["https://www.france-pari.fr/football/france/ligue-1-mcdonald-stm"] * 3,
    ["https://www.france-pari.fr/football/angleterre/premier-league"] * 3,
    ["https://www.france-pari.fr/football/espagne/laliga"] * 3,
    ["https://www.france-pari.fr/football/italie/serie-a"] * 3,
    ["https://www.france-pari.fr/football/allemagne/bundesliga"] * 3
]

# Classes for test website
container_classes = ["no-full-width-container"] * 3
match_classes = ["actors.text-ellipsis"] * 3
odds_classes = ["container-odd-and-trend"] * 3

ligue1_odds = get_ligue1_odds(site_urls[0], container_classes, match_classes, odds_classes)


# Calculates the sum of inverses of odds.
def invsum(x, y, z):
    return 1 / float(x) + 1 / float(y) + 1 / float(z)


# Finds the optimal odds and the corresponding bet distribution.
def maxodds(LA, LB, LC, K, n):
    min_odds = [LA[0][0], LB[0][1], LC[0][2]]
    best_bet = K[0]
    
    for i in range(n):
        for j in range(3):
            k1 = j - 1
            k2 = next(iter({0, 1, 2} - {j, k1}))
            if i >= 8 and (1 - invsum(LA[i][j], LB[i][k1], LC[i][k2])) > (1 - invsum(min_odds[0], min_odds[1], min_odds[2])):
                min_odds[j], min_odds[k1], min_odds[k2] = LA[i][j], LB[i][k1], LC[i][k2]
                best_bet = K[i]
    
    return min_odds, invsum(min_odds[0], min_odds[1], min_odds[2]), best_bet


# Example usage of the maxodds function , 585 whas the amount I was using for the test
L1 = [ligue1_odds[i]["odds"] for i in range(len(site_urls[0]))]
L2 = ligue1_odds[0]["teams"]

odds_result = maxodds(L1[0], L1[1], L1[2], L2, len(L2))
total_bet = 585 / float(odds_result[0][0]) + 585 / float(odds_result[0][1]) + 585 / float(odds_result[0][2])
bet_distribution = 585 / total_bet

print(odds_result, bet_distribution, bet_distribution / float(odds_result[0][0]), bet_distribution / float(odds_result[0][1]), bet_distribution / float(odds_result[0][2]))
