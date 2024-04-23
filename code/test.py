from utils.Scrapper import Scrapper
from utils.gemini import Gemini
import json
import time

def main():
    gemini = Gemini()
    # with open('../data/emails_extracted.json', 'r') as file:
    #     email_content = json.laod(file)
    with open("../data/emails_extracted.json", 'r') as file:
        email_content = json.load(file)  
    count = 0
    for email in email_content:
        content = email['content_plain']
        prompt = f'Determine if the following email content contains misinformation. Answer in either True or False. True indicating that the email content contains misinformation. Limit your answer in one word. \n {content}'
        is_misinfo = gemini.generate(prompt).text
        print(is_misinfo)
        email['is_misinformation'] = 'true' in is_misinfo.lower()
        time.sleep(20)

        prompt = f'Identify the themes and narratives of following email content. Answer in a few key words. \n {content}'
        theme = gemini.generate(prompt).text
        print(theme)
        email['theme'] = theme

        if count >2:
            break
        count +=1
        
        time.sleep(20)
    
    # https://ai.google.dev/tutorials/python_quickstart
    # scrapper = Scrapper(['https://i.stack.imgur.com/Ccnnp.png', 'https://i.stack.imgur.com/Ccnnp2.png'])
    # scrapper.get_all_contents(thread_num=1)
    # print(scrapper.result_map)
    with open("../data/emails_extracted.json", 'w') as file:
        json.dump(email_content, file, indent=4)

if __name__ == '__main__':
    main()
