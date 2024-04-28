# Joan Donovan: Election Narratives-Team B
Haotian Shangguan, Po-han Lu, Mao Mao, Hao Qi, Hui Zheng

## Overview
This repository contains several codes to do the email analysis. There are currently six questions this project aims to accomplish:

1. What themes or narratives is each political party pushing? Does this change by state? 
2. What misinformation or conspiracy theories are different political parties pushing? 
3. What is the sentiment of different campaigns (positive, negative, etc)? 
4. What links are these campaigns sharing?
5. What other people do these emails reference (Donald Trump, Joe Biden, Hilary Clinton, etc)?
6. Do any of these questions change depending on how competitive the seat is?

## Data Preprocess

### Email Extraction
By leveraging the Google API, we systematically extract emails and consolidate them into the [`emails_extracted.json`](./data/emails_extracted.json), categorically organized with key details like email address, sender's name, and plain text content. This structured JSON dataset lays the groundwork for subsequent stages, such as in-depth data analysis.

### Data classification
Once `emails_extracted.json` is in order, we can initiate the classification of senders by their political affiliations and the states they represent. We compile this information into two distinct files: [`All_Senders_Emails.json`](./data/All_senders_Emails.json) and [`Candidates_Emails.json`](./data/Candidate_Emails.json), which facilitate the analysis of each candidate's party and state affiliations. This is achieved by querying each sender's name against the database available at www.fec.gov/search, which provides comprehensive political data. Subsequently, we'll integrate this newly acquired information into `emails_extracted.json` to enrich our dataset. Next, we also did a deep analysis of all the links included in the emails. We collect all the hostnames in all the emails stored in [`hostname.json`](./data/hostname.json) for further data analysis. 

# Data Analysis
Within the [`code`](./code) directory, we have stored individual Python scripts and Jupyter Notebook files corresponding to the six questions previously outlined. Each file contains the solution to a specific question, and we will delve into a more detailed discussion of each file subsequently.

#### [`main_code.ipynb`](./code/main_code.ipynb)
This is a Jupyter Notebook file, and it contains most of the answers to those questions. The first cell is used to retrieve all the emails and store them in the `emails_extracted.json`, and the second cell is used to merge `emails_extracted.json` and `Candidates_Emails.json`. Next, we have covered three questions in the rest of the cells, which are: 

1. what links these campaigns are sharing
2. what other people do these emails reference
3. what is the sentiment of different campaigns

Then, we also included all the visualization code in this file, and you can find them either in the [`result`](./result/) folder or in the rest of the code cells in `main_code.ipynb`. 

#### [`analyze_sentiment.ipynb`](./code/analyze_sentiment.ipynb)
This particular file is dedicated to conducting sentiment analysis for the project. It utilizes the Natural Language Toolkit (nltk) library, employing a Lexicon-based Approach where words are pre-classified as positive or negative. The contents of emails_extracted.json are analyzed to categorize each email's sentiment as positive, negative, or neutral. For additional insights and visual representations, refer to the [`deliverables`](./deliverables/) folder and [`main_code.ipynb`](./code/main_code.ipynb). 

#### [`gemeni.py`](./code/gemini.py)
This file is integral to the project's objective of uncovering political narratives and misinformation. It engages the custom classes `Scrapper` and `Gemini` from the `utils` module, indicating a tailored approach for scraping and processing data. The script parses `emails_extracted.json` to discern prevalent themes and potential misinformation circulated by different political parties, possibly by detecting specific keywords or patterns. This file also includes how we solve these two questions: 

1. What themes or narratives is each political party pushing? Does this change by state?
2. What misinformation or conspiracy theories are different political parties pushing? 

Further elucidation and visualization of the results may be available in the [`deliverables`](./deliverables/) folder and [`main_code.ipynb`](./code/main_code.ipynb). 

#### [`check_trend.ipynb`](./code/check_trend.ipynb)
Lastly, this file is related to the last question, which tries to find out how the sentiments of emails are changed or not in different time periods. Further elucidation and visualization of the results may be available in the [`deliverables`](./deliverables/) folder and [`main_code.ipynb`](./code/main_code.ipynb). 

# Getting Started



# Resources/References
1. Google-API: https://takeout.google.com/u/5/?hl=en&utm_source=ga-ob-search&utm_medium=takeout-card
2. Gemini: https://ai.google.dev/tutorials/python_quickstart
3. Federal Election Commission: https://www.fec.gov/search/
4. Natural Language Toolkit: https://www.nltk.org/
