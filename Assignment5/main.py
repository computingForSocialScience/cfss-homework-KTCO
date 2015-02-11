import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    # YOUR CODE HERE
    
    artist_ids = []
    # Creates a list of artist IDs
    for artist in artist_names:
    	artist_ids.append(fetchArtistId(artist))

    artist_info = []
    # Creates a list of artist info dictionaries
    for ids in artist_ids:
    	artist_info.append(fetchArtistInfo(ids))

    artist_album_ids = []
    # Creates a list of lists of album ids
    for ids in artist_ids:
    	artist_album_ids.append(fetchAlbumIds(ids))

    albums_info = []
    # Creates a list of dictionaries of album information
    for artist_albums in artist_album_ids:
    	for ids in artist_albums:
    		albums_info.append(fetchAlbumInfo(ids))

    # Creates a table from list of dictionaries of artist info
    writeArtistsTable(artist_info)

    # Creates a table from list of dictrionaries of album info
    writeAlbumsTable(albums_info)

    plotBarChart()