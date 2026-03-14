import streamlit as st
import pickle
import pandas as pd

movies_list = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

st.title('Movie Recommendation System')

def recommend(movie):
    index = movies_list[movies_list['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        recommended_movies.append(movies_list.iloc[i[0]].title)
    return recommended_movies


selected_movie = st.selectbox(
    "How would you like to be contacted?",
    movies_list['title'].values,
)
if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    for i in recommendations:
        st.write(i)



