import json
import re

def load_from_JSON_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

all_emails = load_from_JSON_file('data/emails_extracted.json')
all_senders = load_from_JSON_file('data/All_Senders_Emails.json')

email_candidate_map = {}
# Create a map of individual email to candidate object
for sender in all_senders:
    for email in sender['Emails']:
        if email not in email_candidate_map:
            email_candidate_map[email] = sender

newSource_emails = set()
for email in all_emails:
    email_address = re.search(r'<(.+?)>', email['from'])
    if email_address is not None:
        email_address = email_address.group(1)
    else:
        email_address = email['from']

    if email_address not in email_candidate_map:
        newSource_emails.add(email_address)

print(newSource_emails, len(newSource_emails))