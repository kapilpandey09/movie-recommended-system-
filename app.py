import streamlit as st
import pickle 
import pandas as pd
import numpy as np
import sys
import requests

# def fetch_poster(poster_imgs,movie):
#     find_img = movies[movies["title"] == movie]
#     data = poster_imgs[poster_imgs["title"]== find_img].poster_img
    
#     return data

def recommend(movie):
    find_img = movies[movies["title"] == movie]
    # data = poster_imgs[poster_imgs["title"]== find_img].poster_img
    # urls = find_img["poster_img"][0]
    movie_index = find_img.index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    # print(urls)
    print(movie_index)

    # for i in movies_list:
    #     movie_id  = i[0]
    #     # fetch poster from API
    #     movie_name = movies.iloc[movie_id].title
    #     url = poster_imgs[poster_imgs["title"] == movie_name]
    #     urls = url.poster_path[0]
    #     print(urls)
    #     recommend_movies.append(movie_name)
        
    #     recommend_movies_posters.append(urls)
    #     # print(i[0])
    
    for i in movies_list:
        movie_id = i[0]

        movie_name = movies.iloc[movie_id].title

        url = poster_imgs[poster_imgs["title"] == movie_name]

        if not url.empty and pd.notna(url["poster_path"].iloc[0]):
            urls = "https://image.tmdb.org/t/p/w500" + str(url["poster_path"].iloc[0])
        else:
            urls = "https://via.placeholder.com/300x450?text=No+Poster"

        recommend_movies.append(movie_name)
        recommend_movies_posters.append(urls)
    
    print(recommend_movies_posters)
    return recommend_movies,recommend_movies_posters

poster_url = pickle.load(open("poster_url.pkl", 'rb'))
poster_imgs = pd.DataFrame(poster_url)
movies_dict = pickle.load(open("movies_dict.pkl", 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl","rb"))

st.title('Movie Recommender System')


selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
)

if st.button('Recommend'):

    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5  = st.columns(5)

    with col1:
        st.header(names[0])
        st.image(posters[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])
    
    with col4:
        st.header(names[3])
        st.image(posters[3])

    with col5:
        st.header(names[4])
        st.image(posters[4])