import streamlit as st
import pickle
import pandas as pd
import requests

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🎬 MovieFlix Prime")

st.sidebar.info(
    """
    AI Powered Movie Recommendation System

    Technologies Used:

    • Python
    • Pandas
    • NumPy
    • Streamlit
    • Machine Learning

    Dataset:
    • MovieLens
    """
)

# ---------------- LOAD DATA ---------------- #

movies_dict = pickle.load(open("movies.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# ---------------- POSTER FUNCTION ---------------- #

def fetch_poster(movie_name):

    api_key = "abc"

    # Remove year from MovieLens titles
    movie_name = movie_name.split("(")[0].strip()

    url = (
        f"https://api.themoviedb.org/3/search/movie"
        f"?api_key={api_key}"
        f"&query={movie_name}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if len(data["results"]) == 0:
            return None

        poster_path = data["results"][0]["poster_path"]

        if poster_path is None:
            return None

        return (
            "https://image.tmdb.org/t/p/w500"
            + poster_path
        )

    except:
        return None

# ---------------- RECOMMENDATION FUNCTION ---------------- #

def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]

    recommended_movies = []

    for i in movie_list:
        recommended_movies.append(
            movies.iloc[i[0]].title
        )

    return recommended_movies

# ---------------- HEADER ---------------- #

st.markdown(
    """
    <h1 style='text-align:center;color:#E50914;'>
    🎬 Movie Recommendation System
    </h1>

    <p style='text-align:center;font-size:20px;'>
    Discover movies you'll love using AI-powered recommendations
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- SEARCH SECTION ---------------- #

st.subheader("🎥 Search Your Favourite Movie")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend Movies"):

    recommendations = recommend(selected_movie)

    st.subheader(
        f"✨ Because you liked: {selected_movie}"
    )

    cols = st.columns(5)

    for idx, movie in enumerate(recommendations[:5]):

        poster = fetch_poster(movie)

        with cols[idx]:

            if poster:
                st.image(
                    poster,
                    use_container_width=True
                )

            st.caption(movie)

st.markdown("---")

# ---------------- HOMEPAGE RECOMMENDATIONS ---------------- #

st.subheader("🔥 Recommended For You")

default_movie = movies['title'].iloc[0]

try:

    auto_recommendations = recommend(default_movie)

    cols = st.columns(5)

    for idx, movie in enumerate(auto_recommendations[:5]):

        poster = fetch_poster(movie)

        with cols[idx]:

            if poster:
                st.image(
                    poster,
                    use_container_width=True
                )

            st.caption(movie)

except Exception as e:
    st.error(e)

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.caption(
    "Built with Machine Learning, Python and Streamlit"
)
