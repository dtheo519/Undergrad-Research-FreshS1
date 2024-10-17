import json
import nltk
from collections import defaultdict #learn how this actually works and not just implementation.
from nltk.stem import PorterStemmer

#ai generated dictionary of keywords
controversial_keywords = {
    "LGBTQ+": [
        "LGBT", "LGBTQ", "queer", "homosexual", "transgender", 
        "gender identity", "sexual orientation", "same-sex", 
        "non-binary", "gender fluid"
    ],
    "Race and Ethnicity": [
        "race", "racism", "racial", "ethnic", "ethnicity", 
        "discrimination", "prejudice", "stereotype", 
        "diversity", "inclusion", "multicultural"
    ],
    "Gender Issues": [
        "gender", "gender equality", "feminism", "sexism", 
        "misogyny", "patriarchy", "empowerment", 
        "women's rights", "male privilege"
    ],
    "Mental Health": [
        "mental health", "anxiety", "depression", "trauma", 
        "bullying", "self-esteem", "suicide", "addiction"
    ],
    "Politics": [
        "politics", "political", "election", "government", 
        "activism", "protest", "policy", "freedom of speech"
    ],
    "Environmental Issues": [
        "environment", "climate change", "global warming", 
        "sustainability", "pollution", "deforestation"
    ],
    "Religion and Beliefs": [
        "religion", "faith", "spirituality", "beliefs", 
        "Christianity", "Islam", "Buddhism", "Judaism", 
        "superstition", "atheism"
    ],
    "Disability Issues": [
        "disability", "accessible", "handicap", "special needs", 
        "inclusion", "autism", "mental disability"
    ],
    "Body Image and Self-Image": [
        "body image", "self-esteem", "appearance", 
        "weight", "bulimia", "anorexia", "fat-shaming"
    ]
}
ps=PorterStemmer().stem ##faster than making it reinitialize every time
stemmed_keywords = {
    category: {ps(keyword.lower()) for keyword in keywords}
    for category, keywords in controversial_keywords.items()
}
def controversiality_score(review_text):
    score = 0
    found_keywords = defaultdict(list)
    stemmed_review_words = {ps(word) for word in review_text.lower().split()} ##using stems to avoid plurals etc.
    # keyword traverse and search
    for category, keywords in controversial_keywords.items():
        matched_keywords = set(keywords).intersection(stemmed_review_words)
        if matched_keywords:
                found_keywords[category].extend(matched_keywords) #append made it a list inside of a dict (something like that, use extend to add on)
                score += len(matched_keywords)
    
    return score, dict(found_keywords)
outD = []
with open('/home/dom/Documents/Freshman S1/CSCI-Y390/reviews.json', 'r') as file:
    for line in file:
        review = json.loads(line)
        
        # controversity calc/count, return found words etc.
        score, found_keywords = controversiality_score(review.get('review_text', ''))
        if score!=0:
            outD.append({
                "book_id": review.get('book_id', ''), "review_id": review.get('review_id', ''), "controversial_score": score, "keywords_found": found_keywords, "review": (review.get('review_text', '').replace('\n', ' ').replace('\r', '').strip())
            })
# place info into a JSON file
with open('/home/dom/Documents/Freshman S1/CSCI-Y390/controversial_reviews.json', 'w') as out:
    for i in outD:
        out.write(json.dumps(i) + "\n")

