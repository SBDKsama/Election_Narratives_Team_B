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