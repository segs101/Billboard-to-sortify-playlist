from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os



year = input(
    "What year would you like to travel to? Type the date in this year format YYYY-MM-DD==")
spotify_id = os.getenv('spotify_id')
spotify_secret = os.getenv('spotify_secret')
spotify_redirect_url = "http://example.com/"
# scrape data from billboard
response = requests.get(f"https://www.billboard.com/charts/hot-100/{year}")
soup = BeautifulSoup(response.content, "html.parser")
songs = soup.select('#title-of-a-story')
limit = 100
count = 0
filtered_data = []
song_title = [song.get_text().strip() for song in songs]
# List of elements to remove
elements_to_remove = ['Songwriter(s):', 'Producer(s):', 'Imprint/Promotion Label:','Gains in Weekly Performance', 'Additional Awards']

# Iterate through the list and filter elements
for item in song_title:
    if count >= limit:
        break
    elif item not in elements_to_remove:
        filtered_data.append(item)
        count += 1

# Print the filtered list
print(filtered_data)

# Add the filtered songs to a spotify playlist
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com/",
        client_id=spotify_id,
        client_secret=spotify_secret,
        show_dialog=True,
        cache_path="token.txt",
        username=os.getenv('username'),
    )
)
user_id = sp.current_user()["id"]
song_uris = []
for song in filtered_data:
    result = sp.search(q=f"track:{song}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in spotify. Skipped")
playlist = sp.user_playlist_create(user=f"{user_id}", name=f"{year} Billboard Top Tracks", public=False,description=f"Top Tracks from year {year}")

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print("success")
