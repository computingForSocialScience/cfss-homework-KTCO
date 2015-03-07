from flask import Flask, render_template, request, redirect, url_for
import pymysql
from artistNetworks import *
from fetchAlbums import *
from fetchArtist import *
import random

dbname="playlists"
host="127.0.0.2"
user="root"
passwd="Harbinger17"

db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')
c = db.cursor()

app = Flask(__name__)

@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))

@app.route('/playlists/')
def make_playlists_resp():
    c.execute('''SELECT * FROM playlists;''')
    playlists = c.fetchall()
    return render_template('playlists.html',playlists=playlists)

@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
    c.execute('''SELECT * FROM songs
                WHERE playlistId=%s;''',playlistId)
    songs = c.fetchall()
    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']
        # YOUR CODE HERE
        try:
            createNewPlaylist(artistName)
            return(redirect("/playlists/"))
        except LookupError:
            return(redirect("/addPlaylist/"))

#Creates the tables for both playlists and songs in the sql database
sql_playlists = '''CREATE TABLE IF NOT EXISTS 
playlists(id varchar (128), rootArtist nvarchar (128));'''

sql_songs = '''CREATE TABLE IF NOT EXISTS songs 
(playlistId varchar (128), songOrder int, artistName nvarchar (128), 
    albumName nvarchar (128), trackName nvarchar (128));'''

c.execute(sql_playlists)
c.execute(sql_songs)

def createNewPlaylist(artist):
    # finds the max id in playlists and makes the next artist an
    # one more than that or makes the id 1 if there are no artists
    c.execute('''SELECT MAX(id) FROM playlists''')
    max_id_list = c.fetchall()
    if max_id_list[0][0] == None:
        playlist_id = 1
    else:
        max_id = int(max_id_list[0][0])
        playlist_id = max_id+1

    # fetches the artist id using the name given. If the name returns
    # nothing then the definition ends else it continues
    artist_id = fetchArtistId(artist)
    if artist_id == None:
        return
    else:
        # Creates a new sql table using the successfully fetched artist
        fill_table = "INSERT INTO playlists (id, rootArtist) VALUES ('%s','%s');"\
        % (playlist_id, artist)
        c.execute(fill_table)

        # gets a list of related artists 2 deep
        df = getDepthEdges(artist_id,2)
        song_list = []

        #finds 30 random artists from the list and gets information
        for a in range(30):

            # chooses a random artist and fetches info
            artist = random.choice(df)
            info = fetchArtistInfo(artist[1])

            # puts info into variables to be put into a list
            artistName = info['name'].replace("'","''")
            songOrder = a+1
            related_artist = artist[1]
            album_list = fetchAlbumIds(artist[1])
            # I encountered some artists without albums so this is
            # here so it doesn't break
            try:
                album_id = random.choice(album_list)
                album_name = fetchAlbumInfo(album_id)['album_name'].replace("'","''")
                song = fetchRndmSong(album_id).replace("'","''")
            except IndexError:
                album_name = "No Albums"
                song = "No Albums"

            # Creates a tuple and appends it to the list of songs and info
            temp = (playlist_id, songOrder, artistName, album_name, song)
            song_list.append(temp)

        # inserts information into the sql database
        insertQuery = '''INSERT INTO songs (playlistId, songOrder, artistName, 
            albumName, trackName) VALUES (%s, %s, %s, %s, %s);'''
        c.executemany(insertQuery,song_list)

        db.commit()

if __name__ == '__main__':
    app.debug=True
    app.run()


'''Tests'''
#createNewPlaylist("Patti Smith")
#createNewPlaylist("Red Hot Chili Peppers")