import sys
import requests
import csv

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    url = "https://api.spotify.com/v1/search?q="+name+"&type=artist"

    src = requests.get(url)
    id_data = src.json()
    ID = id_data['artists']['items'][0]['id']

    return ID


def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
`   returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    artists_dict = {}

    url = "https://api.spotify.com/v1/artists/"+artist_id

    src = requests.get(url)
    artist_data = src.json()

    artists_dict['followers'] = artist_data['followers']['total']
    artists_dict['genres'] = artist_data['genres']
    artists_dict['id'] = artist_data['id']
    artists_dict['name'] = artist_data['name']
    artists_dict['popularity'] = artist_data['popularity']

    return artists_dict

