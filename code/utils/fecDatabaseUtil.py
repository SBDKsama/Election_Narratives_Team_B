import requests
import requests
from bs4 import BeautifulSoup

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
    