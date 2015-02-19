import sys
import numpy as np
import csv
from io import open
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo, fetchRndmSong
from analyzeNetworks import readEdgeList, degree, combineEdgeLists, pandasToNetworkX, randomCentralNode
from artistNetworks import getRelatedArtists, getDepthEdges, getEdgeList, writeEdgeList

import matplotlib.pyplot as plt

if __name__ == '__main__':
    artist_names = sys.argv[1:]

    # Turns the artist names into artist IDs
    Artist_IDs = []
    for artist in artist_names:
    	Artist_IDs.append(fetchArtistId(artist))

    # Removes None from lists created by invalid artists
    # I addend in an exception to deal with invalid artists in fetchArtistId
    Artist_IDs = [x for x in Artist_IDs if x is not None]

    # Combines edge lists into one master list
    depth = 2
    edgeList = getEdgeList(Artist_IDs[0], depth)
    if len(Artist_IDs) > 1:
        for artist in Artist_IDs[1:]:
            temp = getEdgeList(artist,depth)
            edgeList = combineEdgeLists(edgeList,temp)

    g = pandasToNetworkX(edgeList)

    rndm_artists = []
    for artist in range(30):
        rndm_artists.append(randomCentralNode(g))

    # creates a list of tuples of related (artist,album,song)
    # I altered the code from assignment 5 so that album name
    # is part of the returned dictionary in fetchAlbumInfo and
    # created a new function in fetchAlbums that chooses a random
    # song from an album

    to_write = []
    for artist in rndm_artists:
        albums = fetchAlbumIds(artist)
        rndm_album_id = np.random.choice(albums)
        song_name = fetchRndmSong(rndm_album_id)
        album_info = fetchAlbumInfo(rndm_album_id)
        artist_name = album_info['name']
        album_name = album_info['album_name']
        to_write.append((artist_name, album_name, song_name))
    
    # opens a file, writes the tuples into the csv

    outFile = open('playlist.csv','w',encoding='utf-8')
    outFile.write(u'artist_name,album_name,song_name\n')

    for i in to_write:
        print i
        artist_name = i[0]
        album_name = i[1]
        song_name = i[2]
        outFile.write("%s,\"%s\",%s\n" %\
         (artist_name,album_name,song_name))

    outFile.close()



