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
        return(redirect("/playlists/"))

sql_playlists = '''CREATE TABLE IF NOT EXISTS 
playlists(id varchar (128), rootArtist nvarchar (128));'''

sql_songs = '''CREATE TABLE IF NOT EXISTS songs 
(playlistId varchar (128), songOrder int, artistName nvarchar (128), 
    albumName nvarchar (128), trackName nvarchar (128));'''

c.execute(sql_playlists)
c.execute(sql_songs)

playlist_id = 0

def createNewPlaylist(artist):
    global playlist_id 
    playlist_id = playlist_id + 1

    artist_id = fetchArtistId(artist)
    fill_table = "INSERT INTO playlists (id, rootArtist) VALUES ('%s','%s');"\
    % (playlist_id, artist)
    c.execute(fill_table)

    df = getDepthEdges(artist_id,2)
    song_list = []

    for a in range(30):
        artist = random.choice(df)
        info = fetchArtistInfo(artist[1])

        artistName = info['name'].replace("'","''")
        songOrder = a+1
        related_artist = artist[1]
        album_list = fetchAlbumIds(artist[1])
        try:
            album_id = random.choice(album_list)
        except IndexError:
            album_id = None
        album_name = fetchAlbumInfo(album_id)['album_name'].replace("'","''")
        song = fetchRndmSong(album_id).replace("'","''")
        temp = (playlist_id, songOrder, artistName, album_name, song)
        
        song_list.append(temp)

    insertQuery = '''INSERT INTO songs (playlistId, songOrder, artistName, 
        albumName, trackName) VALUES (%s, %s, %s, %s, %s);'''
    c.executemany(insertQuery,song_list)

    db.commit()

if __name__ == '__main__':
    app.debug=True
    app.run()


'''Tests'''
# createNewPlaylist("Patti Smith")
# createNewPlaylist("Red Hot Chili Peppers")