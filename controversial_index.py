##AI LAYOUT. DO NOT USE. this index is not based on controversial/total, just controversial.
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
with open('/home/dom/Documents/Freshman S1/CSCI-Y390/controversial_reviews.json', 'r') as file:
    reviews = [json.loads(line) for line in file]

book_sentiment = {}

# Sentiment calculator
for review in reviews:
    text = review.get('review', '')
    sentiment_scores = SentimentIntensityAnalyzer().polarity_scores(text)
    sentiment = sentiment_scores['compound']
    book_id = review['book_id']
    controversiality_score = review.get('controversial_score', 0)

    if book_id not in book_sentiment:
        book_sentiment[book_id] = {
            'total_sentiment': 0,
            'count': 0,
            'total_controversiality': 0,
            'controversial_review_count': 0  # Count of controversial reviews
        }

    book_sentiment[book_id]['total_sentiment'] += sentiment
    book_sentiment[book_id]['count'] += 1
    book_sentiment[book_id]['total_controversiality'] += controversiality_score

    # Increment controversial review count if the score is above a threshold
    if controversiality_score >= 1:  # Adjust this threshold as needed
        book_sentiment[book_id]['controversial_review_count'] += 1

# Calculate averages and the controversiality index
average_sentiment = {}
for book_id in book_sentiment:
    total_sentiment = book_sentiment[book_id]['total_sentiment']
    count = book_sentiment[book_id]['count']
    
    average_sentiment[book_id] = {
        'average_sentiment': total_sentiment / count,
        'average_controversiality': book_sentiment[book_id]['total_controversiality'] / count,
        'review_count': count,
        'controversial_review_count': book_sentiment[book_id]['controversial_review_count']
    }

    # Calculate the controversiality index
    # The index formula: (controversial review count) * (negative average sentiment)
    average_sent = average_sentiment[book_id]['average_sentiment']
    index = average_sentiment[book_id]['controversial_review_count'] * (-average_sent if average_sent < 0 else 0)
    average_sentiment[book_id]['controversiality_index'] = index

# Sort the books by controversiality index
sorted_controversiality_index = sorted(average_sentiment.items(), key=lambda x: x[1]['controversiality_index'], reverse=True)

# Create the dictionary for JSON format
sorted_sentiment_list = []
for book_id, stats in sorted_controversiality_index:
    sorted_sentiment_list.append({
        'book_id': book_id,
        'average_sentiment': stats['average_sentiment'],
        'average_controversiality': stats['average_controversiality'],
        'review_count': stats['review_count'],
        'controversial_review_count': stats['controversial_review_count'],
        'controversiality_index': stats['controversiality_index']
    })

# Output
with open('/home/dom/Documents/Freshman S1/CSCI-Y390/controversial_sorted_average_sentiment.json', 'w') as outfile:
    for i in sorted_sentiment_list:
        outfile.write(json.dumps(i) + "\n")  # Single line output
