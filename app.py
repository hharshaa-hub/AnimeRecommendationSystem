import pandas as pd
import pickle
import streamlit as st
from recommender import get_recommendations
import random  # Import random module

# Load processed data and cosine similarity matrix
df_anime = pd.read_csv("final_updated_anime_data_with_posters.csv")
with open("cosine_sim.pkl", "rb") as f:
    cosine_sim = pickle.load(f)

# Streamlit UI setup
st.set_page_config(page_title="Anime Recommender", layout="wide")
st.title("🎌 Anime Recommendation System")

# Dropdown to select anime
anime_list = df_anime['anime_title'].sort_values().unique()
selected_anime = st.selectbox("Choose an anime to get recommendations:", anime_list)

# Default image URLs list
default_images = [
    "https://s3.eu-west-1.amazonaws.com/images.geeknative.com/wp-content/uploads/2023/03/21210917/music-films-toho-at-10.jpg",
    "https://thepopblogph.com/wp-content/uploads/2021/02/anime-copy.png",  
    "https://example.com/path/to/third_image.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRR5tlxCcelo5rGd-FZbWwDinaYDwthFR2cyA&s",
    "https://preview.redd.it/g4149co9g6451.jpg?width=640&crop=smart&auto=webp&s=f61c7aa982c600660a208178d649ba181b1b5d88",
    "https://i.pinimg.com/736x/c9/2b/1e/c92b1e71c8adceb19bfdcbcab18ad12a.jpg",
    "https://i.quotev.com/ud55tqvuvdbq.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZ_gOGbMO90vUZhmROmWm-Vq-WyUQVuPDJxg&s",
    "https://images.saymedia-content.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:eco%2Cw_1200/MTc0Mjg1ODYwMTU2NDgzMDY4/why-do-i-like-anime.jpg",
    "https://static1.srcdn.com/wordpress/wp-content/uploads/2024/11/joysound-top-10-anime-characters.jpg",
    "https://preview.redd.it/question-what-are-some-of-your-favourite-character-designs-v0-wps4hyddqusa1.jpg?width=640&crop=smart&auto=webp&s=67c601dc626314d3cbb23ed917092e48910109bc"  
]

# Recommend button and logic
if st.button("Recommend"):
    recommendations = get_recommendations(selected_anime, df_anime, cosine_sim)

    if isinstance(recommendations, str):
        st.warning(recommendations)
    else:
        st.write("### Recommended Anime:")
        for _, row in recommendations.iterrows():
            with st.container():
                cols = st.columns([1, 3])
                with cols[0]:
                    # Randomly select a default image from the list
                    poster_url = row['anime_poster'] if pd.notna(row['anime_poster']) and row['anime_poster'].startswith("http") else random.choice(default_images)
                    st.image(poster_url, width=200)  # Set width to 200px or any other size
                with cols[1]:
                    st.markdown(f"**[{row['anime_title']}]({row['anime_urls']})**")
                    st.markdown(f"⭐ **Rating**: `{row['anime_mal_score']:.1f}/10`")
                    st.markdown(f"🔥 **Popularity Score**: `{row['popularity_score']:.2f}`")
                    if pd.notna(row['anime_overview']):
                        st.markdown(f"📝 **Overview**: {row['anime_overview']}")
                    else:
                        st.markdown("📝 **Overview**: Not available.")
            st.markdown("---")
