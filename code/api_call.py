import re

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tqdm import tqdm
import os.path
import pickle
import base64
import json

# Use pip install --upgrade google-auth-oauthlib google-auth-httplib2 google-api-python-client
# to install the required packages

# If modifying these SCOPES, delete the file token.pickle.pi
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


# Use the credentials.json file from the Gmail API to authenticate
def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service


# Remove URLs, non-ASCII characters, multiple spaces, newlines, and carriage returns
def clean_email_content(content):
    if (content is None or content == '' or len(content) == 0):
        return content
    # Remove URLs
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    content = url_pattern.sub('', content)

    # Remove non-ASCII characters
    unicode_pattern = re.compile(r'[^\x00-\x7F]+')
    content = unicode_pattern.sub('', content)

    # Remove multiple spaces
    multiple_spaces_pattern = re.compile(r'\s\s+')
    content = multiple_spaces_pattern.sub(' ', content)

    # Remove empty square brackets
    empty_brackets_pattern = re.compile(r'\[\s*\]')
    content = empty_brackets_pattern.sub('', content)

    # Remove newlines and carriage returns
    content = content.replace('\r', '').replace('\n', '')

    # Remove consecutive symbols e.g ||| !!!!! -----
    consecutive_symbol_pattern = re.compile(r'(\W)\1{2,}')
    content = consecutive_symbol_pattern.sub(r'\1', content)

    return content.strip()


# Get the message from the Gmail API
def get_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        payload = message['payload']
        headers = payload.get("headers")
        subject = [header['value'] for header in headers if header['name'] == 'Subject'][0]
        date = [header['value'] for header in headers if header['name'] == 'Date'][0]  # Extract the date
        labels = message.get('labelIds', [])  # Extract the labels
        from_email = [header['value'] for header in headers if header['name'] == 'From'][0]  # Extract the from email
        delivered_to = [header['value'] for header in headers if header['name'] == 'Delivered-To'][0]  # Extract the delivered_to email
        parts = payload.get("parts")
        body = ''
        if parts:
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
        else:
            data = payload['body']['data']
            body = base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
        return {'from': from_email, 'delivered_to': delivered_to, 'subject': subject, 'date': date, 'labels': labels, 'content_plain': clean_email_content(body)}
    except Exception as e:
        print(f'An error occurred: {e}')
        return None


# Fetch the most recent emails and save them as JSON
def get_recent_emails_and_save_as_json(service, user_id='me', max_results=5):
    results = service.users().messages().list(userId=user_id, maxResults=max_results, labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
    else:
        for i, message in enumerate(messages):
            email_info = get_message(service, user_id, message['id'])
            if email_info:
                file_path = f'../data/email_{i + 1}.json'
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(email_info, file, ensure_ascii=False, indent=4)
                print(f"Saved email {message['id']} to {file_path}")


# Fetch all emails and save them as JSON
def get_all_emails_and_save_as_json(service, user_id='me'):
    # Get the total number of messages in the user's mailbox
    profile = service.users().getProfile(userId=user_id).execute()
    total_messages = profile['messagesTotal']
    print(f"Total number of messages: {total_messages}")

    page_token = None
    all_emails = []  # Create an empty list to store all email details

    # Initialize the progress bar with the total number of messages
    progress_bar = tqdm(total=total_messages, desc="Processing emails")

    while True:
        results = service.users().messages().list(userId=user_id, pageToken=page_token, labelIds=['INBOX']).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No messages found.")
            break
        else:
            for message in messages:
                email_info = get_message(service, user_id, message['id'])
                if email_info:
                    all_emails.append(email_info)  # Append the email details to the list
                # Update the progress bar
                progress_bar.update(1)

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    # Close the progress bar
    progress_bar.close()

    # Save all email details to a single JSON file
    with open('../data/emails_extracted.json', 'w', encoding='utf-8') as file:
        json.dump(all_emails, file, indent=4)


if __name__ == '__main__':
    # Get the Gmail API service
    service = get_gmail_service()

    # Fetch the most recent 5 emails and save them as JSON
    # get_recent_emails_and_save_as_json(service)
    get_all_emails_and_save_as_json(service)
