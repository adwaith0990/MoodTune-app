import streamlit as st
import pandas as pd

# ============================================
# PAGE SETTINGS
# ============================================

st.set_page_config(
    page_title="MoodTune",
    page_icon="🎵",
    layout="wide"
)

# ============================================
# LOAD DATASET
# ============================================

df = pd.read_csv("spotify_tracks.csv")

# Remove missing values
df = df.dropna()

# ============================================
# CREATE MOOD DETECTION
# ============================================

def detect_mood(row):

    # Happy songs
    if row['valence'] > 0.6 and row['energy'] > 0.6:
        return 'Happy'

    # Sad songs
    elif row['valence'] < 0.4 and row['energy'] < 0.5:
        return 'Sad'

    # Workout songs
    elif row['energy'] > 0.7:
        return 'Workout'

    # Party songs
    elif row['danceability'] > 0.7:
        return 'Party'

    # Chill songs
    else:
        return 'Chill'

# Create new Mood column
df['Mood'] = df.apply(detect_mood, axis=1)

# ============================================
# TITLE
# ============================================

st.title("🎧 MoodTune")
st.subheader("AI Powered Mood Based Music Recommendation")

# ============================================
# SIDEBAR
# ============================================

st.sidebar.title("🎵 Select Your Mood")

mood = st.sidebar.selectbox(
    "Choose Mood",
    ["Happy", "Sad", "Chill", "Workout", "Party"]
)

# ============================================
# FILTER SONGS
# ============================================

filtered_df = df[df['Mood'] == mood]

# ============================================
# RECOMMEND BUTTON
# ============================================

if st.button("Recommend Songs 🎶"):

    st.success(f"Showing {mood} Songs")

    # Random 5 songs
    recommendations = filtered_df.sample(5)

    for index, row in recommendations.iterrows():

        st.markdown("---")

        # Song Name
        st.write(f"## 🎵 {row['track_name']}")


        # Artist Name
        if 'track_artist' in df.columns:
            st.write("🎤 Artist:", row['track_artist'])

        # Album Name
        if 'album_name' in df.columns:
            st.write("💿 Album:", row['album_name'])

        # Spotify Player
        if 'track_id' in df.columns:

            spotify_url = f"https://open.spotify.com/embed/track/{row['track_id']}"

            st.components.v1.iframe(
                spotify_url,
                height=80
            )