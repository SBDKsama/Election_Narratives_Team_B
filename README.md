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
In 

# Getting Started



# Resources/References
1. Google-API: https://takeout.google.com/u/5/?hl=en&utm_source=ga-ob-search&utm_medium=takeout-card
2. Gemini: https://ai.google.dev/tutorials/python_quickstart
3. Federal Election Commission: https://www.fec.gov/search/
4. Natural Language Toolkit: https://www.nltk.org/







Please submit your final project submission PR (to your team branch) by Saturday evening (04/27) for the 1st round of review. The following should be done before submitting your PR:
A brief description at the top of each code file explaining how the code contributes to your analysis
Comments throughout your code where relevant
A README that includes the following:
A section explaining what base/extended questions you have answered and your results
A section detailing your data cleaning methods with links to the files for data cleaning
A section explaining your data analysis with links to the files for data analysis
Links to datasets (Done)
A section for resources/references (Done)
A section explaining how to run your code/how to reproduce your results [I will be following this to make sure your code runs, so please ensure it is nicely explained :)]


