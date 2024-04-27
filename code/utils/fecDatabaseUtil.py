# Summary:
# The `fecDatabaseUtil.py` script contains a function `queryFec` that fetches party and state information for a given candidate from the FEC (Federal Election Commission) website.

# Description:
# - The function `queryFec` accepts a candidate's name as input and performs an HTTP GET request to the FEC's search page to retrieve data about the candidate.
# - It uses the BeautifulSoup library to parse the HTML response from the FEC website.
# - The script looks for HTML elements that match certain criteria (e.g., `<li>` tags with class `post`) to extract relevant information about the candidate.
# - Specific details such as the candidate's state and party are extracted from the HTML and returned.
# - If no relevant information is found, default values of 'unknown' are assigned for both state and party.
# - This function is essential for enhancing candidate data by providing additional contextual information about their political affiliations and geographic representation.
# - Error handling or specific validations are not detailed in the excerpt but would be critical to ensure robustness and reliability of data scraping in a real-world application.

import requests
import requests
from bs4 import BeautifulSoup

# This function is using to request the party and state by given the candidate's name through the website called www.fec.gov.
def queryFec(candidateName):
    response = requests.get(
        'https://www.fec.gov/search/',
        params={
            'query': candidateName,
            'type': 'candidates'
        }
    )
    # print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    # Find all 'li' elements with class 'post'
    posts = soup.find_all('li', class_='post')

    # Loop through each post and extract the required information
    state_info = 'unknown'
    party = 'unknown'
    for post in posts:
        # Find all spans with class 'entity__type'
        entity_types = post.find_all('span', class_='entity__type')

        # Extract the text from the first span and compare it with 'Candidate for Senate'
        if entity_types[0].text.strip() != 'Candidate for Senate':
            continue
        
        # The second span contains the state (and possibly district information)
        state_info = entity_types[1].text.strip()
        
        # The third span contains the political party
        party = entity_types[2].text.strip().split(' ')[0]
    return state_info, party

# Example usage
print('Jacky Rosen', queryFec('Jacky Rosen'))
    