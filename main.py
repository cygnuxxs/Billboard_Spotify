from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Enter the date that you want fetch the top 100 songs (YYYY-MM-DD): ")

#Scrapping top 100 songs from Billboard into a list

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(response.text, "html.parser")
songs = soup.find_all(id = "title-of-a-story", class_ = "a-no-trucate")
songs = [song.getText().replace("\t", "").replace("\n", "") for song in songs]

#Spotify Authentication
id = '55e26f2b843546bca0c67c23ff07c652'
secret = "d89cde98eda146b9bdc99e379e66164f"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=id,
    client_secret=secret,
    scope="playlist-modify-private",
    show_dialog=True,
    redirect_uri="http://example.com"
))
user = sp.current_user()["id"]

#Searching Spotify for songs by title
songs_uri = []
total = 0
year = date.split("-")[0]
for song in songs:
    result = sp.search(q = f"track:{song}", type="track", limit=2)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
        total += 1
        print(f"\"{song}\" is added ({total}/100).")
    except IndexError:
        print(f"\"{song}\" is not found in Spotify, Skipped.")

#Creating a private playlist in Spotify
playlist = sp.user_playlist_create(user=user, name=f"{date} Billboard 100", public=False)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uri)
print(f"{total}/100 songs are added to your playlist.")
print("Done.")