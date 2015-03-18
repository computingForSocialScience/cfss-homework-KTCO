from flask import Flask, render_template, request, redirect, url_for
from io import open
from create_tables import *
from uploads_create_tables import *
from create_graph import create_undirected_graph
import create_tables
import pymysql
import pandas as pd
import networkx as nx
import json
import matplotlib.pyplot as plt 
import warnings

dbname="facebook"
host="127.0.0.2"
user="root"
passwd="Harbinger17"

db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')
c = db.cursor()

# Flask Portion

app = Flask(__name__)

@app.route('/')
def make_index_resp():
	db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')
	c = db.cursor()
	# creates a list of friends on the webpage
	c.execute('''SELECT uid, name FROM friend_info ORDER BY name;''')
	friend_info = c.fetchall()
	return(render_template('index.html',friend_info=friend_info))
 
@app.route('/profile/<uid>/')
# takes an uid and finds information about them from the SQL server
def make_profiles(uid):
	db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')
	c = db.cursor()
	# gets information about each person from SQL server
	c.execute('''SELECT name, sex, affiliations, birthday,
	hometown_location, current_location, relationship_status, 
	significant_other_id, political, religion, profile_url, pic 
	FROM friend_info 
	WHERE uid=%s;''',uid)
	friend_info = c.fetchall()

	# finds the name of the person
	name = friend_info[0][0]
	name_list = []
	# finds all of the names of friends from the server by looking in both
	# uid1 and uid2 column
	c.execute('''SELECT * FROM friend_edges
		WHERE uid1=%s;''',name)
	friend_edge_uid1=c.fetchall()

	for friend in friend_edge_uid1: 
		name_list.append(friend[1])

	c.execute('''SELECT * FROM friend_edges
		WHERE uid2=%s;''',name)
	friend_edge_uid2=c.fetchall()
	
	for friend in friend_edge_uid2:
		name_list.append(friend[0])

	# sorts the names alphabetically
	name_list.sort()
	# my name does not have a uid associated with which throws some errors
	try:
		name_list.remove("Kevin On")
	except ValueError:
		pass
	
	uid_list = []
	# finds all uids associated with each name
	for friend in name_list:
		c.execute('''SELECT uid FROM friend_info WHERE name=%s;''',friend)
		uid_info = c.fetchall()
		if not uid_info:
			continue
		else:
			uid_list.append(uid_info[0][0])
	
	# combines both name list and uid list to be used in the html
	uid_name = []
	for i in range(len(uid_list)):
		cat = (uid_list[i],name_list[i])
		uid_name.append(cat)

	plot_name = create_undirected_graph(name)

	return(render_template('profiles.html',friend_info=friend_info,\
		uid_name=uid_name,plotPng=plot_name))

@app.route('/upload/',methods=['GET','POST'])
def make_upload():
	if request.method == 'GET':
		return render_template('upload.html') 
	elif request.method == 'POST':
		friend_edges = request.files['edges']
		upload_attributes = request.files['attributes']

		upload_create_edge_table(friend_edges)
		upload_create_attributes_table(upload_attributes) 

	 	return (redirect("/")) 

if __name__ == '__main__':
    app.debug=True 
    app.run() 