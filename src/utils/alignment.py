# Alignment utilities
"""
Utility functions for aligning and matching data.
"""

import difflib


def find_closest_match(word, lst):
    """
    Finds the closest match to the given word from a list of words.
    
    Args:
        word (str): Word to find match for
        lst (list): List of words to search in
    
    Returns:
        str: The closest match found
    """
    matches = difflib.get_close_matches(word, lst, cutoff=0)
    if matches:
        return matches[0]
    return word  # Return the original word if no match found


def align_lists_by_closeness(lists, lists2, n):
    """
    Swaps elements in each list based on their closeness to the reference list.
    
    Args:
        lists (list): Lists of team names to be aligned
        lists2 (list): Lists of odds to be aligned along with team names
        n (int): Number of lists to process
    
    Returns:
        tuple: Tuple of aligned lists (teams, odds)
    """
    reference_list = lists[0]
    
    for index, word in enumerate(reference_list):
        for j in range(1, n):
            closest_match = find_closest_match(word, lists[j])
            closest_match_index = lists[j].index(closest_match)
            lists[j][index], lists[j][closest_match_index] = lists[j][closest_match_index], lists[j][index]
            lists2[j][index], lists2[j][closest_match_index] = lists2[j][closest_match_index], lists2[j][index]

    return lists, lists2


def find_min_teams(data, n):
    """
    Finds the minimum number of teams across all data lists.
    
    Args:
        data (list): List of dictionaries containing team data
        n (int): Number of data sources
    
    Returns:
        int: Minimum number of teams
    """
    min_teams = len(data[0]["teams"])
    for i in range(n):
        if len(data[i]["teams"]) < min_teams:
            min_teams = len(data[i]["teams"])
    return min_teams