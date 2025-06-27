import pickle
import streamlit as st
import requests


st.set_page_config(page_title="Movie Recommendation System", layout="wide")

# Background Image (movie-themed)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #c4c4c4
        background-attachment: fixed;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎬 Movie Recommendation System")






# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=00b1e4356d28998263943fc5dc0ad4af&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path



def fetch_poster(movie_id, api_key="00b1e4356d28998263943fc5dc0ad4af"):
    if not movie_id:
        print("Invalid movie_id:", movie_id)
        return None

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    print("Fetching:", url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
             print("No poster path in API response.")
             return None
    except requests.exceptions.RequestException as e:
        print("Error fetching poster:", e)
        return None





def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1:6])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


# st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)



if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Make sure we have at least 5 recommendations
    num_recs = min(5, len(recommended_movie_posters))
    cols = st.columns(num_recs)

    for i in range(num_recs):
        if recommended_movie_posters[i] is not None:
            with cols[i]:
                st.image(recommended_movie_posters[i])
                st.text(recommended_movie_names[i])
