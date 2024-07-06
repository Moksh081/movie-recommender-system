import pickle
import streamlit as st
import requests
import os
import pandas as pd

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')

# Update paths to your files
movie_list_path = 'D:/movie-recommender-system/movie_dict.pkl'
similarity_path = 'D:/movie-recommender-system/similarity.pkl'

if not os.path.exists(movie_list_path) or not os.path.exists(similarity_path):
    st.error("Model files are missing. Please ensure 'movie_dict.pkl' and 'similarity.pkl' are in the 'D:/movie-recommender-system' directory.")
else:
    movies_dict = pickle.load(open(movie_list_path, 'rb'))
    similarity = pickle.load(open(similarity_path, 'rb'))
    
    # Convert the dictionary to a DataFrame
    movies = pd.DataFrame(movies_dict)
    
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        
        if recommended_movie_posters[0]:
            with col1:
                st.text(recommended_movie_names[0])
                st.image(recommended_movie_posters[0])
        
        if recommended_movie_posters[1]:
            with col2:
                st.text(recommended_movie_names[1])
                st.image(recommended_movie_posters[1])
        
        if recommended_movie_posters[2]:
            with col3:
                st.text(recommended_movie_names[2])
                st.image(recommended_movie_posters[2])
        
        if recommended_movie_posters[3]:
            with col4:
                st.text(recommended_movie_names[3])
                st.image(recommended_movie_posters[3])
        
        if recommended_movie_posters[4]:
            with col5:
                st.text(recommended_movie_names[4])
                st.image(recommended_movie_posters[4])
