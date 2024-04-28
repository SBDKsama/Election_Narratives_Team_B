# Summary:
# The `emailUtil.py` script provides utility functions for handling email data, including parsing email addresses and names from email strings, and manipulating JSON data related to emails.

# Description:
# - The function `load_from_JSON_file` reads and returns data from a JSON file, which is useful for handling data persistence or configuration settings.
# - `getEmailAddress` extracts the email address from a string that may contain additional formatting or text around the email address, using regular expressions to find patterns that match typical email formats.
# - `getNameAddressPair` extracts both the name and the email address from a string, cleaning up the name by removing excess characters and normalizing its format.
# - `getFirstMiddleLast` splits a full name into its constituent parts (first, middle, last), which is useful for data processing or when interfacing with systems that require these components separately.
# - `updateAllSenderEmailsJson` is a function that presumably updates or processes a list of email data stored in JSON format, reflecting changes or additions to the data set.
# - This script facilitates efficient handling and processing of email-related data, useful in applications where email data extraction and manipulation are required.

import json
import re

from candidate import addStateAndPartyInfoToCandidateJson

def load_from_JSON_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def getEmailAddress(email_from):
    email_address = re.search(r'<(.+?)>', email_from)
    if email_address is not None:
        email_address = email_address.group(1)
    else:
        email_address = email_from
    return email_address

def getNameAddressPair(email_from):
    email_address = getEmailAddress(email_from)
    name = email_from.replace('<' + email_address + '>', '').replace('Team', '').replace('"', '').title().strip()
    # print(name, '-' , email_address, '-',email_from)
    return name, email_address

def getFirstMiddleLast(name):
    name = name.split()
    first = name[0]
    last = name[-1]
    middle = ' '.join(name[1:-1])
    return first, middle, last

def updateAllSenderEmailsJson():
    all_emails = load_from_JSON_file('data/emails_extracted.json')
    all_senders = load_from_JSON_file('data/All_Senders_Emails.json')

    # Create a map of individual email to candidate object
    # for example, Jane Doe <jd@gmail.com, doej@hotmail.com> will be mapped to 
    # {jd@gmail.com, Jane Doe} and {doej@hotmail.com, Jane Doe}
    existing_email_candidate_map = {}
    for sender in all_senders:
        for email in sender['Emails']:
            if email not in existing_email_candidate_map:
                existing_email_candidate_map[email] = sender

    # readin all the emails and check if the sender email is in the email_candidate_map
    # if not, add it to the new_email_address_set
    new_name_from_map = {} # email_address -> email['from'], E.g. 'jd@gmail.com' -> 'Jane Doe <jd@gmail.com>'
    address_content_map = {}
    for email in all_emails:
        name, email_address = getNameAddressPair(email['from'])
        name_address_pair = (name, email_address)
        if email_address not in existing_email_candidate_map:
            new_name_from_map[name] = email['from']
        
        if email_address not in address_content_map: 
            address_content_map[name_address_pair] = []
        address_content_map[name_address_pair].append(email['content_plain'])

    # print('New sender found: \n', new_name_address_map, '\nCount:', len(new_name_address_map))

    # check the sender name one by one manually and update the email_candidate_map
    name_emailAddrs_map = {}
    for name in new_name_from_map:
        email_address = getEmailAddress(new_name_from_map[name])
        # first, middle, last = getFirstMiddleLast(name)
        # print(first, middle, last)
        if name not in name_emailAddrs_map:
            name_emailAddrs_map[name] = []
        name_emailAddrs_map[name].append(email_address)

    print('new candidate identified:',len(name_emailAddrs_map))
    # with the new email candidate array, ask the user to confirm the name and email address
    new_email_candidate_array = []
    for name in name_emailAddrs_map:
        first, middle, last = getFirstMiddleLast(name)
        print(f"First: {first}, Middle: {middle}, Last: {last}, Emails: {name_emailAddrs_map[name]}")
        confirmation = input("Is this correct? Yes, No, Correction Needed(y/n/c): ")
        if confirmation.lower() == 'y':
            candidate = {
                'First': first,
                'Middle': middle,
                'Last': last,
                'Emails': name_emailAddrs_map[name]
            }
        elif confirmation.lower() == 'c':
            correct_first = input("Please enter the correct First name: ")
            correct_middle = input("Please enter the correct Middle name: ")
            correct_last = input("Please enter the correct Last name: ")
            candidate = {
                'First': correct_first,
                'Middle': correct_middle,
                'Last': correct_last,
                'Emails': name_emailAddrs_map[name]
            }
        else: 
            continue
        all_senders.append(candidate)
        new_email_candidate_array.append(candidate)

    if len(new_email_candidate_array) != 0:
        print(new_email_candidate_array)


    # Save the new email candidate array to data/All_Senders_Emails.json
    with open('data/All_Senders_Emails.json', 'w') as file:
        json.dump(all_senders, file, indent=4)


def updateCandidatesEmailsJson():
    non_candidate_list = ['Secure', 'Google', 'Wordpress', 'Brady PAC', 'Campaign', 'Wix']
    all_senders = load_from_JSON_file('data/All_Senders_Emails.json')
    candidates = load_from_JSON_file('data/Candidates_Emails.json')

    # Create a set of existing first and last names from all_senders
    existing_names = set()
    for candidate in candidates:
        existing_names.add((candidate['First'], candidate['Last']))

    # Check if each candidate's first and last name is in the existing_names set
    missing_candidates = []
    for sender in all_senders:
        if (sender['First'], sender['Last']) not in existing_names and sender['First'] not in non_candidate_list:
            missing_candidates.append(sender)

    # Add the missing candidates to all_senders
    candidates.extend(missing_candidates)

    # Print out the new added entries
    if len(missing_candidates) > 0:
        print("Newly added entries:")
        for candidate in missing_candidates:
            print(candidate)

    # Save the updated all_senders to data/All_Senders_Emails.json
    with open('data/Candidates_Emails.json', 'w') as file:
        json.dump(candidates, file, indent=4)
    
    # add party and state info to the candidate json
    addStateAndPartyInfoToCandidateJson()

# updateAllSenderEmailsJson()

updateCandidatesEmailsJson()



