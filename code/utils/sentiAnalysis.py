# Summary:
# The `sentiAnalysis.py` file contains a class `SentimentAnalyzer` that utilizes the VADER sentiment analysis tool from the NLTK library.
# This class is designed to evaluate the sentiment of a given text and classify it as positive, negative, or neutral.

# Description:
# - The `SentimentAnalyzer` class initializes an instance of `SentimentIntensityAnalyzer`.
# - If the necessary VADER lexicon is not found during initialization, it is downloaded automatically.
# - The `fit` method takes a string of text as input and computes sentiment scores using the VADER tool.
# - The method evaluates the 'compound' score to categorize the overall sentiment:
#   - Positive if the compound score is above 0.05.
#   - Negative if the compound score is below -0.05.
#   - Neutral if the compound score is between -0.05 and 0.05.
# - The result includes both the raw scores (positive, negative, neutral, and compound) and the sentiment category.
# - This setup ensures that the class can easily be utilized to assess sentiment in various contexts, potentially as part of a larger text processing or content analysis framework.

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        try:
            self.analyzer = SentimentIntensityAnalyzer()
        except LookupError:
            print(f"! sentiAnalysis.py: VADER not found, running nltk.download('vader_lexicon') now ...")
            nltk.download('vader_lexicon')
            self.analyzer = SentimentIntensityAnalyzer()
    
    '''
    description: 
        Using VADER (Valence Aware Dictionary and sEntiment Reasoner), analyze 
        the sentiment of the input text
    param {Str} text from `content_plain`
    return {Dict}   different scores
    return {Str}    general sentiment classification result
    '''    
    def fit(self, text):
        sentiment_scores = self.analyzer.polarity_scores(text)

        compound_score = sentiment_scores['compound']
        if compound_score >= 0.05:
            sentiment_category = 'positive'
        elif compound_score <= -0.05:
            sentiment_category = 'negative'
        else:
            sentiment_category = 'neutral'

        return sentiment_scores, sentiment_category

