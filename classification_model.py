import pandas as pd
import re
import nltk
import numpy as np

# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score

data = pd.read_csv(r"C:\Users\LENOVO\Desktop\Movie DB with NLP\IMDB Dataset.csv")

corpus = []
for i in range(len(data)):
    review = re.sub('[^a-zA-Z]', ' ', data['review'][i])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()

    temp = stopwords.words('english')
    not_stopword = {"weren't",'shouldn','haven','isn',"wasn't", "won't",'needn', 'doesn','aren', 'nor','won','ain', "aren't", "couldn't",'hadn', 'mustn', "mustn't", 'no', 'not', "hasn't", "needn't", "shouldn't", 'didn', 'couldn', "hadn't","isn't", "don't", 'hasn', "wouldn't", 'wouldn', 'mightn', "haven't", 'weren', "didn't","mightn't", 'wasn', "doesn't"}
    
    for t in not_stopword:
        if(t in temp):
            temp.remove(t)
    
    temp.append("br")
    review = [ps.stem(word) for word in review if not word in set(temp)]

    review = ' '.join(review)
    corpus.append(review)

cv = CountVectorizer(max_features=65000,binary=True)
X = cv.fit_transform(corpus)
y = data['sentiment'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

classifier = LogisticRegression()
classifier.fit(X_train, y_train)
result = classifier.predict(X_test)

print(confusion_matrix(result, y_test))
print(accuracy_score(result, y_test))

import joblib 
joblib.dump((classifier,cv),"model_trained")