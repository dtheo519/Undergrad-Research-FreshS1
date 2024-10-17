import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
with open('/home/dom/Documents/Freshman S1/CSCI-Y390/controversial_reviews.json', 'r') as file:
    reviews = [json.loads(line) for line in file]

book_sentiment = {}

#sentiment calculator 
for review in reviews:
    text = review.get('review_text', '')
    sentiment_scores = SentimentIntensityAnalyzer().polarity_scores(text) 
    sentiment = sentiment_scores['compound'] 
    book_id = review['book_id']
        
    if book_id not in book_sentiment:
        book_sentiment[book_id] = {
            'total_sentiment': 0,
            'count': 0
        }
        
        # score count
    book_sentiment[book_id]['total_sentiment'] += sentiment
    book_sentiment[book_id]['count'] += 1

# averages all reviews on a per book basis 
average_sentiment = {}
for book_id in book_sentiment:
    total_sentiment = book_sentiment[book_id]['total_sentiment']
    count = book_sentiment[book_id]['count']
    average_sentiment[book_id] = total_sentiment / count

# not really sure. i think this is lowest to highest?
sorted_average_sentiment = sorted(average_sentiment.items(), key=lambda x: x[1], reverse=True)

# creates the dictionary for json format
sorted_sentiment_list = []
for book_id, avg_sentiment in sorted_average_sentiment:
    sorted_sentiment_list.append({
        'book_id': book_id, 'average_sentiment': avg_sentiment, 'review_count': book_sentiment[book_id]['count']
    })

# output
with open('/home/dom/Documents/Freshman S1/CSCI-Y390/controversial_sorted_average_sentiment.json', 'w') as outfile:
    for i in sorted_sentiment_list:
        outfile.write(json.dumps(i)+"\n") ##single line output, i think something is wrong here!!!

#Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.