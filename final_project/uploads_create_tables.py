from flask import Flask, render_template, request, redirect, url_for
from io import open
import pymysql
import pandas as pd
import networkx as nx
import json
import matplotlib.pyplot as plt 
import tempfile
import warnings

dbname="facebook"
host="127.0.0.2"
user="root"
passwd="Harbinger17"

db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')
c = db.cursor()


def upload_get_edge_data(edges):
	uid = []
	# loads a file in json format
	friend_edge_data = json.load(edges)

	# creates a list of tuples of names
	for i in friend_edge_data:
		uid.append((i['uid1'],i['uid2']))
	return uid

def upload_get_friend_info(attributes):
	friend_info = []

	# loads a file in json format
	friend_info_data = json.load(attributes)
	info_list = []

	# loops through loaded json data and creates a list of lists of information
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

		# getting affiliations if empty list fills in with none
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

		# getting home town if empty fills in with none
		home = i['hometown_location']
		if home != None:
			home_string = home['name']+', '+home['country']
		else:
			home_string = None
		temp_info.append(home_string)

		# getting current location, if empty fills in with none
		cur_loc = i['current_location']
		if cur_loc != None:
			current_location_string = cur_loc['name']+', '+cur_loc['country']
		else:
			current_location_string = None
		temp_info.append(current_location_string)

		# getting relationship_status, if empty fills in with none
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

def upload_create_edge_table(edges):
	# deletes current sql table
	sql_delete = ''' DELETE FROM friend_edges;'''
	c.execute(sql_delete)
	# Gets data in the form of a list of tuples
	uid = upload_get_edge_data(edges)

	# Inserts data into SQL table
	insertQuery = '''INSERT INTO friend_edges(uid1, uid2) VALUES (%s, %s);'''
	c.executemany(insertQuery,uid)
	db.commit()

def upload_create_attributes_table(attributes):
	# deletes data in sql table
	sql_delete = ''' DELETE FROM friend_info;'''
	c.execute(sql_delete)
	
	# gets info from json file
	friend_attributes = upload_get_friend_info(attributes)

	# inserts data into SQL table
	insertQuery = '''INSERT INTO friend_info(uid, name, sex, affiliations,
				birthday, hometown_location, current_location, relationship_status,
				significant_other_id, political, religion, locale, profile_url, pic)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
	c.executemany(insertQuery, friend_attributes)
	db.commit()

