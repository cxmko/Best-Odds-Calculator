# Odds scraper module
"""
Web scraper for retrieving sports betting odds from various websites.
"""

import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from src.utils.text_processing import (
    split_list_by_newline, replace_comma_with_period, 
    remove_vs, remove_empty_elements, find_first_non_tuple_index
)
from src.utils.alignment import find_min_teams, align_lists_by_closeness


class OddsScraper:
    def __init__(self, webdriver_path="chromedriver"):
        """
        Initialize the OddsScraper with the path to the webdriver.
        
        Args:
            webdriver_path (str): Path to the Chrome webdriver executable
        """
        self.webdriver_path = webdriver_path
        self.options = Options()
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--headless')  # Run browser in headless mode
    
    def get_odds(self, site_urls, container_classes, match_classes, odds_classes, start_idx=0, end_idx=9999):
        """
        Scrapes odds and teams data from multiple websites.
        
        Args:
            site_urls (list): List of URLs to scrape
            container_classes (list): List of container class names for each site
            match_classes (list): List of match class names for each site
            odds_classes (list): List of odds class names for each site
            start_idx (int): Starting index for slicing results
            end_idx (int): Ending index for slicing results
        
        Returns:
            list: List of dictionaries containing teams and their odds
        """
        service = Service(self.webdriver_path)
        driver = webdriver.Chrome(service=service, options=self.options)
        
        all_data = []
        
        for url, container_class, match_class, odds_class in zip(site_urls, container_classes, match_classes, odds_classes):
            driver.get(url)
            time.sleep(5)  # Wait for page to load
            
            containers = driver.find_elements(By.CLASS_NAME, container_class)    
            site_data = {'teams': [], 'odds': []}
            
            for container in containers:
                i, j = 1, 2
                team_elements = container.find_elements(By.CLASS_NAME, match_class)
                teams = [remove_vs(i.text.strip()) for i in team_elements]
                teams = split_list_by_newline(teams)
                
                # Format team names as "Team1 vs Team2"
                while i < len(teams):
                    teams[i-1] += " vs " + teams[i]
                    del teams[i]
                    i += 1
                
                odd_elements = container.find_elements(By.CLASS_NAME, odds_class)
                odds = [replace_comma_with_period(i.text.strip()) for i in odd_elements]
                odds = remove_empty_elements(odds)
                
                # Backup method to extract odds if the text is empty
                if not odds:
                    for element in odd_elements:
                        raw_text = element.get_attribute("innerHTML")
                        match_odds = re.search(r'\d+,\d+', raw_text)
                        if match_odds:
                            odd_value = match_odds.group(0)
                            odd_value = replace_comma_with_period(odd_value)
                            if 1.01 < float(odd_value) < 20:  # Validate odds are reasonable
                                odds.append(odd_value)
                
                # Group odds into tuples (home, draw, away)
                while j < len(odds) and j <= len(teams) + 1:
                    odds[j] = (odds[j-2], odds[j-1], odds[j])
                    del odds[j-1]
                    del odds[j-2]
                    j += 1

                # Keep only valid tuple odds
                odds = odds[:find_first_non_tuple_index(odds)]
                
                # Apply slicing
                actual_end = min(len(teams), end_idx)
                teams, odds = teams[start_idx:actual_end], odds[start_idx:actual_end]
                
                site_data['teams'].extend(teams)
                site_data['odds'].extend(odds)
            
            all_data.append(site_data)
        
        driver.quit()
        
        # Align data across different sites
        min_teams = find_min_teams(all_data, len(site_urls))
        reference_teams = all_data[0]["teams"][:min_teams]
        
        teams_lists = [all_data[i]["teams"][:min_teams] for i in range(len(site_urls))]
        odds_lists = [all_data[i]["odds"][:min_teams] for i in range(len(site_urls))]
        
        aligned_data = align_lists_by_closeness(teams_lists, odds_lists, len(site_urls))
        
        # Update data with aligned results
        for i in range(len(site_urls)):
            all_data[i]["teams"], all_data[i]["odds"] = reference_teams, aligned_data[1][i]
        
        return all_data