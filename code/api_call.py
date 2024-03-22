from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
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

# Get the message from the Gmail API
def get_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        payload = message['payload']
        headers = payload.get("headers")
        subject = [header['value'] for header in headers if header['name'] == 'Subject'][0]
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
        return {'id': msg_id, 'subject': subject, 'body': body}
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
                file_path = f'../data/email_{i+1}.json'
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(email_info, file, ensure_ascii=False, indent=4)
                print(f"Saved email {message['id']} to {file_path}")


# Fetch all emails and save them as JSON
def get_all_emails_and_save_as_json(service, user_id='me'):
    page_token = None
    i = 0
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
                    file_path = f'../data/email_{i+1}.json'
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(email_info, file, ensure_ascii=False, indent=4)
                    print(f"Saved email {message['id']} to {file_path}")
                i += 1

        page_token = results.get('nextPageToken')
        if not page_token:
            break


# Get the Gmail API service
service = get_gmail_service()

# Fetch the most recent 5 emails and save them as JSON
get_recent_emails_and_save_as_json(service)
# get_all_emails_and_save_as_json(service)
