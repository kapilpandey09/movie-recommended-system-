import streamlit as st
import pickle
import pandas as pd



st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)



st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.movie-card {
    background-color: #1c1f26;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 10px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.3);
}

.movie-title {
    color: white;
    font-size: 16px;
    font-weight: bold;
    min-height: 70px;
    text-align: center;
    margin-top: 10px;
}

div.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 10px;
    font-size: 18px;
    font-weight: bold;
    background: linear-gradient(90deg,#ff4b4b,#ff6b6b);
    color: white;
    border: none;
}

</style>
""", unsafe_allow_html=True)


poster_url = pickle.load(open("poster_url.pkl", "rb"))
poster_imgs = pd.DataFrame(poster_url)

movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))


def recommend(movie):

    movie_data = movies[movies["title"] == movie]

    movie_index = movie_data.index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for item in movies_list:

        movie_id = item[0]

        movie_name = movies.iloc[movie_id].title

        poster = poster_imgs[
            poster_imgs["title"] == movie_name
        ]

        if not poster.empty and pd.notna(
            poster["poster_path"].iloc[0]
        ):
            poster_url = (
                "https://image.tmdb.org/t/p/w500"
                + poster["poster_path"].iloc[0]
            )
        else:
            poster_url = (
                "https://via.placeholder.com/300x450"
                "?text=No+Poster"
            )

        recommended_movies.append(movie_name)
        recommended_posters.append(poster_url)

    return recommended_movies, recommended_posters



st.markdown(
    """
    <h1 style='text-align:center;color:white'>
    🎬 Movie Recommendation System
    </h1>

    <p style='text-align:center;color:gray;font-size:18px'>
    Discover movies similar to your favorite films
    </p>
    """,
    unsafe_allow_html=True
)



# st.image(
#     "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba",
#     use_container_width=True
# )

# st.write("")



selected_movie_name = st.selectbox(
    "🎥 Select a Movie",
    movies["title"].values
)



if st.button("🔍 Recommend Movies"):

    with st.spinner("Finding similar movies..."):

        names, posters = recommend(selected_movie_name)

    st.write("")
    st.subheader("Recommended Movies")

    cols = st.columns(5)

    for idx, col in enumerate(cols):

        with col:

            st.markdown(
                "<div class='movie-card'>",
                unsafe_allow_html=True
            )

            st.image(
                posters[idx],
                use_container_width=True
            )

            st.markdown(
                f"""
                <div class='movie-title'>
                {names[idx]}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )