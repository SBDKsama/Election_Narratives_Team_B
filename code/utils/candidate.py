# Summary:
# The `candidate.py` script is designed to update a JSON file containing candidate information with additional details fetched from an FEC database.

# Description:
# - The script includes a function `updateCandidateJson` that reads from a JSON file (`data/emails_extracted.json`), which presumably contains details about various candidates.
# - It uses a function `queryFec` imported from `fecDatabaseUtil` to fetch additional data for each candidate, specifically the state and party affiliation based on the candidate's name.
# - This additional information is added to each candidate's entry in the dictionary extracted from the JSON file.
# - After updating the dictionary with new data, the script writes the updated content back to the JSON file, ensuring the original data structure is maintained but enhanced with new details.
# - This process involves both reading from and writing to a file, with JSON handling for data storage.
# - The approach allows for efficient updating of candidate information in a structured format, facilitating easy access and manipulation of the data for further applications.

from fecDatabaseUtil import queryFec
import json

def updateCandidateJson():
    candidates_and_emails = 'data/emails_extracted.json'
    with open(candidates_and_emails, 'r', encoding='utf-8') as email_book:
        candidate_email_dict = json.load(email_book)

    # BEGIN: Add state and party field to email_book
    for candidate in candidate_email_dict:
        candidate['state'], candidate['party']  = queryFec(candidate['Last'] + ' ' + candidate['First'])
    # END: Add state and party field to email_book
        
    # Open the file in write mode
    with open(candidates_and_emails, 'w', encoding='utf-8') as email_book:
        # Dump the updated dictionary back into the JSON file
        json.dump(candidate_email_dict, email_book, ensure_ascii=False, indent=4)

updateCandidateJson()