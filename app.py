import pickle
import streamlit as st
import requests
import os

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movies.pkl','rb'))

import os
import pickle
import streamlit as st
import requests

def download_file_from_google_drive(id, destination):
    """
    Handles large Google Drive files
    """
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={'id': id}, stream=True)
    token = None

    # Check for large file warning
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    # Save the file
    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# ------------------------
similarity_file = "similarity.pkl"
file_id = "1BAUn42HxPL6mKEBj2OaDL2IfpNZW0zK5"  # Your Google Drive file ID

if not os.path.exists(similarity_file):
    st.info("Downloading similarity matrix, please wait...")
    download_file_from_google_drive(file_id, similarity_file)
    st.success("Download complete!")

with open(similarity_file, "rb") as f:
    similarity = pickle.load(f)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Create 5 columns
    cols = st.columns(5)

    # Loop through the recommended movies and their posters
    for idx, col in enumerate(cols):
        col.text(recommended_movie_names[idx])
        col.image(recommended_movie_posters[idx])




