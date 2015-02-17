import requests
import pandas as pd


def getRelatedArtists(artistID):
	# Takes an artist ID and returns a list of related artists IDs

	url = "https://api.spotify.com/v1/artists/"\
	+artistID+"/related-artists"

	src = requests.get(url)
	related_artists_src = src.json()
	related_artists = related_artists_src['artists']

	IDs = []
	for artist in related_artists:
		IDs.append(artist['id'])

	return IDs	

def getDepthEdges(artistID, depth):
	# Takes an artist ID and the depth of the search and returns
	# a list of tuples of related artists
	
	artist_pairs = []
	for i in range(depth):
		artists = getRelatedArtists(artistID)
		for artist in artists:
			artist_pairs.append((artistID,artist))
			if (depth-1)==0:
				pass
			else:
				artist_pairs=artist_pairs+(getDepthEdges(artist,(depth-1)))
	return artist_pairs

def getEdgeList(artistID,depth):
	# Takes an artist ID, depth of search and returns an a Pandas DataFrame

	artist_depth_list=getDepthEdges(artistID,depth)
	artist_df = pd.DataFrame.from_records(artist_depth_list,
		columns=['Artist IDs','Related Artists IDs'])
	rm_duplicates = artist_df.drop_duplicates()
	return rm_duplicates

def writeEdgeList(artistID,depth,filename):
	# Takes artist ID, depth, and filename and returns a csv file with 
	# pandas data frame written in it

	df=getEdgeList(artistID,depth)
	return pd.DataFrame.to_csv(df,filename+".csv",index=False)


# writeEdgeList("2PtMZoO4GEp2JEN3pxbTmO",1,"Edge_Test2")
# writeEdgeList("2mAFHYBasVVtMekMUkRO9g",1,"Edge_Test")
# writeEdgeList("2mAFHYBasVVtMekMUkRO9g",2,"Edge_Test")
# print(getEdgeList("2mAFHYBasVVtMekMUkRO9g",2))
# print(getDepthEdges("2mAFHYBasVVtMekMUkRO9g",2))
# print(getRelatedArtists("2mAFHYBasVVtMekMUkRO9g"))
