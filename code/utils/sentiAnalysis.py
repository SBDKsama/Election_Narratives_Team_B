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

