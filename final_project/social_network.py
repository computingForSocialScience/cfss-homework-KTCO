
from flask import Flask, render_template, request, redirect, url_for
from io import open
import pymysql
import json
import warnings

dbname="facebook"
host="127.0.0.2"
user="root"
passwd="Harbinger17"

db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')
c = db.cursor()

app = Flask(__name__)

def get_edge_data():
	uid = []
	json_data = open("friend_edges.json")
	friend_edge_data = json.load(json_data)
	json_data.close()

	for i in friend_edge_data:
		uid.append((i['uid1'],i['uid2']))
	return uid

def get_friend_info():
	friend_info = []
	friend_data = open("friend_attributes.json")
	friend_info_data = json.load(friend_data)
	friend_data.close()

	info_list = []

	for i in friend_info_data:
		temp_info = []

		# getting uid
		uid = i['uid']
		temp_info.append(uid)

		# getting name
		name = i['name']
		temp_info.append(name.replace("'","''"))

		# getting sex
		sex = i['sex']
		temp_info.append(sex)

		# getting affiliations
		affiliations = i['affiliations']
		if affiliations == None or not affiliations:
			temp = None
		else:
			temp = []
			for each in affiliations:
				temp.append(each['type']+': '+each['name'])
			temp = ' | '.join(temp)
		temp_info.append(temp)		

		# getting birthday
		birthday = i['birthday']
		temp_info.append(birthday)

		# getting home town
		home = i['hometown_location']
		if home != None:
			home_string = home['name']+', '+home['country']
		else:
			home_string = None
		temp_info.append(home_string)

		# getting current location
		cur_loc = i['current_location']
		if cur_loc != None:
			current_location_string = cur_loc['name']+', '+cur_loc['country']
		else:
			current_location_string = None
		temp_info.append(current_location_string)

		# getting relationship_status
		relationship_status = i['relationship_status']
		if relationship_status == "":
			relationship_status = None
		temp_info.append(relationship_status)

		# getting significant other
		significant_other_id = i['significant_other_id']
		temp_info.append(significant_other_id)

		# getting political
		political = i['political']
		temp_info.append(political)

		# getting religion
		religion = i['religion']
		temp_info.append(religion)

		# getting locale
		locale = i['locale']
		temp_info.append(locale)

		# getting profile_url
		profile_url = i['profile_url']
		temp_info.append(profile_url)

		# getting prof pic
		pic = i['pic']
		temp_info.append(pic)
		
		info_list.append(temp_info)
	return info_list

with warnings.catch_warnings():
	warnings.simplefilter("error")
	try:
		sql_friend_edges = '''CREATE TABLE IF NOT EXISTS 
		friend_edges(uid1 nvarchar (128), uid2 nvarchar (128));'''

		c.execute(sql_friend_edges)
	
		uid = get_edge_data()
		insertQuery = '''INSERT INTO friend_edges(uid1, uid2) VALUES (%s, %s);'''
		c.executemany(insertQuery,uid)
	except Warning:
		pass

with warnings.catch_warnings():
	warnings.simplefilter("error")
	try:
		sql_friend_info = '''CREATE TABLE IF NOT EXISTS friend_info
		(uid nvarchar (128), name nvarchar (128), sex varchar (64), affiliations nvarchar (128),
			birthday nvarchar (128), hometown_location nvarchar (128),
			current_location nvarchar(128), relationship_status varchar(64),
			significant_other_id nvarchar (128), political nvarchar (128), religion nvarchar(128),
			locale nvarchar(128), profile_url nvarchar(128), pic nvarchar(256))'''		
		
		c.execute(sql_friend_info)

		friend_attributes = get_friend_info()
		insertQuery = '''INSERT INTO friend_info(uid, name, sex, affiliations,
			birthday, hometown_location, current_location, relationship_status,
			significant_other_id, political, religion, locale, profile_url, pic)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
		c.executemany(insertQuery, friend_attributes)
	except Warning:
		pass

# Flask Portion of the 
@app.route('/')
def make_index_resp():
	c.execute('''SELECT uid, name FROM friend_info ORDER BY name;''')
	friend_info = c.fetchall()
	return(render_template('index.html',friend_info=friend_info))

@app.route('/profile/<uid>/')
def make_profiles(uid):
	c.execute('''SELECT * FROM friend_info 
		WHERE uid=%s;''',uid)
	friend_info = c.fetchall()
	return(render_template('profiles.html',friend_info=friend_info))

db.commit()

if __name__ == '__main__':
    app.debug=True
    app.run()