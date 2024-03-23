import streamlit as st
import requests
import json
import re
import nltk
from nltk.stem.porter import PorterStemmer
import joblib

nltk.download('stopwords')
from nltk.corpus import stopwords
temp = stopwords.words('english')
not_stopword = {"weren't",'shouldn','haven','isn',"wasn't", "won't",'needn', 'doesn','aren', 'nor','won','ain', "aren't", "couldn't",'hadn', 'mustn', "mustn't", 'no', 'not', "hasn't", "needn't", "shouldn't", 'didn', 'couldn', "hadn't","isn't", "don't", 'hasn', "wouldn't", 'wouldn', 'mightn', "haven't", 'weren', "didn't","mightn't", 'wasn', "doesn't"}
    
for t in not_stopword:
    if(t in temp):
        temp.remove(t)

model,cv = joblib.load('model_trained')

st.sidebar.title("FilmFlix: Your Gateway to Cinematic Adventures")
radio = st.sidebar.radio("What information you want : ",["Homepage","Movie Details","TV Shows and series","Movie review prediction"])

if radio == "Homepage":
    st.title("Welcome to the amazing world of Moviezzzz....")
    
    image1 = "pic1.jpg"
    image2 = "pic2.jpg"
    col1, col2 = st.columns(2)
    with col1:
        st.image(image1,width=350)

    with col2:
        st.image(image2,width=350)

    image3 = "pic3.jpg"
    image4 = "pic4.jpg"
    col1, col2 = st.columns(2)
    with col1:
        st.image(image3,width=350)

    with col2:
        st.image(image4,width=350)




elif radio == "Movie Details":
    st.header("Find your favourite movie details here....")
    name = st.text_input("Enter the name of the movie")
    year = st.text_input("Enter the year of the release")
    search = st.button("Search movie")
    if search:
        url = "https://api.themoviedb.org/3/search/movie?api_key=ed39a40df6bb03fa9a89ec96222957e6&query="+name+"&year="+year

        data = requests.get(url).text
        data = json.loads(data)

        movies = data['results']
        if len(movies) == 0:
            st.error("Error no movie found... Please check the name or year properly and try again")
        else: 
            for movie in movies :
                st.markdown("---")
                poster_path = movie['poster_path']
                if poster_path != None:
                    image_url = "https://image.tmdb.org/t/p/w500"+poster_path
                    st.image(image_url,width=220)
                st.header(movie['title'])
                st.info(movie['overview'])
                st.text("Released on : "+movie['release_date'])
                st.text("Number of ratings : "+str(movie['vote_count']))
                st.text("Average ratings : "+str(movie['vote_average'])+'⭐')
                st.markdown("---")



elif radio == "TV Shows and series":
    st.header("Find your favourite serials and web series details here....")
    name = st.text_input("Enter the name of the series")
    # year = st.text_input("Enter the year of the release")
    search = st.button("Search series")
    if search:
        url = "https://api.themoviedb.org/3/search/tv?api_key=ed39a40df6bb03fa9a89ec96222957e6&query="+name

        data = requests.get(url).text
        data = json.loads(data)

        series = data['results']
        if len(series) == 0:
            st.text("Error no series found... Please check the name or year properly and try again")
        else: 
            for serial in series :
                st.markdown("---")
                poster_path = serial['poster_path']
                if poster_path != None:
                    image_url = "https://image.tmdb.org/t/p/w500"+poster_path
                    st.image(image_url,width=200)
                st.header(serial['name'])
                st.info(serial['overview'])
                st.text("Released on : "+serial['first_air_date'])
                st.text("Number of ratings : "+str(serial['vote_count']))
                st.text("Average ratings : "+str(serial['vote_average'])+'⭐')
                st.markdown("---")



else:
    st.header("Find your next movie to watch....")
    name = st.text_input("Enter the name of the movie")
    year = st.text_input("Enter the year of the release")
    search = st.button("Explore people's reviews ")

    if search:
        url = "https://api.themoviedb.org/3/search/movie?api_key=ed39a40df6bb03fa9a89ec96222957e6&query="+name+"&year="+year

        data = requests.get(url).text
        data = json.loads(data)
        movie = data['results']
        if len(movie) == 0:
            st.error("Error no movie found... Please check the name or year properly and try again")
        else:
            movie = movie[0]
            st.markdown("---")
            poster_path = movie['poster_path']
            if poster_path != None:
                image_url = "https://image.tmdb.org/t/p/w500"+poster_path
                st.image(image_url,width=200)
            st.header(movie['title'])
            st.info(movie['overview'])
            
            movie_id = movie['id']
            review_url = "https://api.themoviedb.org/3/movie/"+str(movie_id)+"/reviews?api_key=ed39a40df6bb03fa9a89ec96222957e6"

            reviews = requests.get(review_url).text
            reviews = json.loads(reviews)
            reviews = reviews['results']
            if len(reviews) == 0:
                st.error("No user reviews found")
                st.text("The ratings are as follows")
                st.text("Number of ratings : "+str(movie['vote_count']))
                st.text("Average ratings : "+str(movie['vote_average'])+'⭐')
            else:    
                positive = 0
                negative = 0
                total = len(reviews)
                for review in reviews:
                    # review is of type string 
                    review = review['content']
                    review = re.sub('[^a-zA-Z]', ' ', review)
                    review = review.lower()
                    review = review.split()
                
                    ps = PorterStemmer()
                    review = [ps.stem(word) for word in review if not word in set(temp)]
                    review = ' '.join(review)
                    review = cv.transform([review]).toarray()
                    ans = (model.predict(review))[0]
                    if ans == 'positive':
                        positive = positive + 1
                    else:
                        negative = negative + 1
                st.subheader("Total reviews : "+str(total))
                st.success("Positive reviews : "+str(positive))
                st.error("Negative reviews : "+str(negative))

                if(positive > negative):
                    st.info("Hey...the people are liking the movie...🎉")
                elif(positive < negative):
                    st.info("Hey...the people have not liked the movie...🥺")
                else:
                    st.info("Hey... the movie stands a 50 - 50 chance...🤔")           
