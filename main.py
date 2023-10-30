import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --SCRAPE BILLBOARD TOP 100 using beautifulsoup library and create a list of the top 100 songs----------
BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"
response = requests.get(BILLBOARD_URL)
data = response.text
soup = BeautifulSoup(data, "html.parser")
song_titles = soup.select(selector="ul li h3")
songs = [each.getText().strip() for each in song_titles if song_titles.index(each) < 100]


# -----ADD SPOTIFY DEVELOPER APP and AUTHORIZE YOURSELF
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
authorization = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://example.org",
    scope="playlist-modify-private",)

app = spotipy.Spotify(auth_manager=authorization)


# -- FROM BILLBOARD TOP 100 SONG LIST SEARCH FOR EACH SONG'S ID USING SPOTIFY API----
user_id = app.current_user()["id"]
songs_id = []
for song in songs:
    result = app.search(q=f"track:{song}", type="track")
    try:
        songs_id.append(result["tracks"]["items"][0]["album"]["id"])
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Hence not added.")


# -----CREATE SPOTIFY PLAYLIST and ADD THE TOP 100 SONGS TO THE NEWLY CREATED LIST
playlist = app.user_playlist_create(user=user_id, name=f"Billboard 100", public=False)
app.playlist_add_items(playlist_id=f"{playlist['id']}", items=songs_id)
