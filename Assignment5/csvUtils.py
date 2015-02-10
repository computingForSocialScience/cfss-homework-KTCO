from io import open
import csv
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo

def writeArtistsTable(artist_info_list):
    """Given a list of dictionries, each as returned from 
    fetchArtistInfo(), write a csv file 'artists.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
    """
    outFile = open('artists.csv','w') 
    output = []

    outFile.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n')
    for i in range(len(artist_info_list)):
        curr = artist_info_list[i]
        ID = curr['id']
        name = curr['name']
        followers = curr['followers']
        popularity = curr['popularity']
        outFile.write("%s,\"%s\",%d,%d\n" % (ID,name,followers,popularity))

    outFile.close()
      
def writeAlbumsTable(album_info_list):
    """
    Given list of dictionaries, each as returned
    from the function fetchAlbumInfo(), write a csv file
    'albums.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
    """
    outFile = open('albums.csv','w')
    output = []
    outFile.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY')
    
    for i in range(len(album_info_list)):
        curr = album_info_list[i]
        outFile.write("%s,%s,\"%s\",%s,%d\n"%\
            (curr['artist_id'],curr['album_id'],\
            curr['name'],curr['year'],curr['popularity']))

    outFile.close()