import requests
from datetime import datetime
from fetchArtist import fetchArtistId

def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url = "https://api.spotify.com/v1/artists/"+artist_id+"/albums"\
    "?album_type=album&market=US"
    src = requests.get(url)
    album_data = src.json()
    albums = [album_data['items'][i]['id']\
    for i in range(len(album_data['items']))]

    return albums

#fetchAlbumIds(fetchArtistId("Regina Spektor"))

def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    album_dict = {}

    url = "https://api.spotify.com/v1/albums/"+album_id

    src = requests.get(url)
    album_data = src.json()

    album_dict['artist_id'] = album_data['artists'][0]['id']
    album_dict['album_id'] = album_data['id']
    album_dict['name'] = album_data['artists'][0]['name']
    album_dict['year'] = album_data['release_date'][0:4]
    album_dict['popularity'] = album_data['popularity']

    return album_dict



# tests
# print(fetchAlbumInfo(fetchAlbumIds(fetchArtistId("Regina Spektor"))[0]))
# print(fetchAlbumInfo(fetchAlbumIds(fetchArtistId("Patti Smith"))[0]))