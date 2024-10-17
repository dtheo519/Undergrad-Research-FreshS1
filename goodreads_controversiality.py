import json
import nltk
from collections import defaultdict
from nltk.stem import PorterStemmer

# AI-generated dictionary of keywords
controversial_keywords = {
    "LGBTQ+": ["LGBT", "LGBTQ", "queer", "homosexual", "transgender", 
               "gender identity", "sexual orientation", "same-sex", 
               "non-binary", "gender fluid"],
    "Race and Ethnicity": ["race", "racism", "racial", "ethnic", "ethnicity", 
                           "discrimination", "prejudice", "stereotype", 
                           "diversity", "inclusion", "multicultural"],
    "Gender Issues": ["gender", "gender equality", "feminism", "sexism", 
                      "misogyny", "patriarchy", "empowerment", 
                      "women's rights", "male privilege"],
    "Mental Health": ["mental health", "anxiety", "depression", "trauma", 
                      "bullying", "self-esteem", "suicide", "addiction"],
    "Politics": ["politics", "political", "election", "government", 
                 "activism", "protest", "policy", "freedom of speech"],
    "Environmental Issues": ["environment", "climate change", "global warming", 
                             "sustainability", "pollution", "deforestation"],
    "Religion and Beliefs": ["religion", "faith", "spirituality", "beliefs", 
                             "Christianity", "Islam", "Buddhism", "Judaism", 
                             "superstition", "atheism"],
    "Disability Issues": ["disability", "accessible", "handicap", "special needs", 
                          "inclusion", "autism", "mental disability"],
    "Body Image and Self-Image": ["body image", "self-esteem", "appearance", 
                                   "weight", "bulimia", "anorexia", "fat-shaming"]
}

ps = PorterStemmer().stem
stemmed_keywords = {
    category: {ps(keyword.lower()) for keyword in keywords}
    for category, keywords in controversial_keywords.items()
}

def controversiality_score(review_text):
    score = 0
    found_keywords = defaultdict(list)
    stemmed_review_words = {ps(word) for word in review_text.lower().split()}
    # Keyword traverse and search
    for category, keywords in controversial_keywords.items():
        matched_keywords = set(keywords).intersection(stemmed_review_words)
        if matched_keywords:
            found_keywords[category].extend(matched_keywords)
            score += len(matched_keywords)
    
    return score, dict(found_keywords)

outD = []
with open('/home/dom/Documents/Freshman S1/CSCI-Y390/data/reviews.json', 'r') as file:
    for line in file:
        review = json.loads(line)
        
        # Controversity calc/count, return found words etc.
        score, found_keywords = controversiality_score(review.get('review_text', ''))
        if score != 0:
            outD.append({
                "book_id": review.get('book_id', ''),
                "review_id": review.get('review_id', ''),
                "controversial_score": score,
                "keywords_found": found_keywords,
                "review": review.get('review_text', '').replace('\n', ' ').replace('\r', '').strip()
            })

# Place info into a JSON array
with open('/home/dom/Documents/Freshman S1/CSCI-Y390/data/revised/controversial_reviews.json', 'w') as out:
    json.dump(outD, out, indent=4)  # Write the list as a JSON array
