from flask import Flask, render_template, request, redirect, url_for
from io import open
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

app = Flask(__name__)

# Flask Portion
UPLOAD_FOLDER = '/home/Kevin/cfss/cfss-homework-KTCO/final_project/uploads'
ALLOWED_EXTENSIONS = set(['json'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def make_index_resp():
	c.execute('''SELECT uid, name FROM friend_info ORDER BY name;''')
	friend_info = c.fetchall()
	return(render_template('index.html',friend_info=friend_info))

@app.route('/profile/<uid>/')
def make_profiles(uid):
	c.execute('''SELECT name, sex, affiliations, birthday,
	hometown_location, current_location, relationship_status, 
	significant_other_id, political, religion, profile_url, pic 
	FROM friend_info 
	WHERE uid=%s;''',uid)
	friend_info = c.fetchall()

	name = friend_info[0][0]
	name_list = []

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

	name_list.sort()
	name_list.remove("Kevin On")
	
	uid_list = []
	for friend in name_list:
		c.execute('''SELECT uid FROM friend_info WHERE name=%s;''',friend)
		uid_info = c.fetchall()
		if not uid_info:
			continue
		else:
			uid_list.append(uid_info[0][0])
	
	uid_name = []
	for i in range(len(uid_list)):
		cat = (uid_list[i],name_list[i])
		uid_name.append(cat)

	return(render_template('profiles.html',friend_info=friend_info,uid_name=uid_name))

@app.route('/upload',methods=['GET','POST'])
def make_upload():
	if request.method == 'GET':
		return render_template('upload.html')
	elif request.method == 'POST':
		upload_edges = request.files['file']
		upload_attributes = request.files['file']
		if upload_edges and allowed_file(upload_edges.filename):
			upload_edges.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		if upload_attributes and allowed_file(upload_attributes.filename):
			upload_attributes.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

		# f=open('upload_edges','w')
		# json.dump(upload_edges,f)
		# f.close()

		# create_edge_table('upload_edges.json')

if __name__ == '__main__':
    app.debug=True
    app.run()