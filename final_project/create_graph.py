import pymysql
import pandas as pd
import networkx as nx
import json
import matplotlib.pyplot as plt 
import warnings
import tempfile

dbname="facebook"
host="127.0.0.2"
user="root"
passwd="Harbinger17"

db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')
c = db.cursor()

edgeList = pd.read_sql("SELECT * FROM friend_edges",db)
# Undirected Graphs: 
# takes a name, returns a list of friends
def create_friends_list(name):
	# finds edges containing the given name
	uid1 = edgeList.query('uid1==["%s"]' % name)
	uid2 = edgeList.query('uid2==["%s"]' % name)
	# creates a friends list
	friends_list = []
	for name in uid1['uid2'].iteritems():
		friends_list.append(name[1])
	for name in uid2['uid1'].iteritems():
		friends_list.append(name[1])
	
	return friends_list

# takes a name and creates a graph and returns a graph name
def create_undirected_graph(name):
	# creates a network graph
	g = nx.Graph()
	# finds all edges containing the given name
	uid1 = edgeList.query('uid1==["%s"]' % name)
	uid2 = edgeList.query('uid2==["%s"]' % name)
	
	# concatenates the edges into a single list
	uid = pd.concat([uid1,uid2])
	# adds edges to graph
	for uid1, uid2 in uid.to_records(index=False):
		g.add_edge(uid1,uid2)
	
	# creates a list of friends for the given name
	friends_list = create_friends_list(name)

	dict_list = []
	# for each friend in the friends list, it finds mutual friends
	for friend in friends_list:
		# creates a friend list for a person on the original friend list
		temp = create_friends_list(friend)
		# compares friend lists
		temp_friends = list(set(temp) & set(friends_list))
		# creates a dictionary of mutual friends
		for each in temp_friends:
			edge = {"uid1":friend,"uid2":each}
			dict_list.append(edge)
	# turns the mutual friends into a data frame
	new_edges = pd.DataFrame(dict_list)

	# adds edges for new mutual friends
	for uid1, uid2 in new_edges.to_records(index=False):
		g.add_edge(uid1,uid2)

	# specifies a layout
	Layout = nx.layout.random_layout(g)
	# draws the figure
	nx.draw(g,pos=Layout, with_labels="uid1",\
	node_size=25,font_size=5,width=0.1,node_color='b',hold=None)

	f = tempfile.NamedTemporaryFile(
		dir='static/temp',
		suffix='.png',delete=False)
	# saves the figure
	plt.savefig(f,dpi=150)
	# clears figure
	plt.clf()
	f.close

	# random name for the figure
	plotPng = f.name.split('\\')[-1]
	return plotPng