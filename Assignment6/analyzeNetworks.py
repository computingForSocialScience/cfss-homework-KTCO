import requests
import pandas as pd
import networkx as nx
import numpy as np

def readEdgeList(filename):
	# Takes a file name and reads the file and returns a data from of the file
	
	Edge_df = pd.read_csv(filename)
	shape = Edge_df.shape
	df = pd.DataFrame.from_records(Edge_df)
	if shape[1] != 2:
		print ("Incorrect Number of Columns")
		return df.iloc[:,:2]
	elif shape[1] < 2:
		print("Incorrect Number of Columns")
		return df
	else:
		return df

def degree(edgeList, in_or_out):
	# Takes an edge list data frame and a string "in" or "out" denoting
	# which degree to return

	df = edgeList
	first_col = df.iloc[:,[0]]
	second_col = df.iloc[:,[1]]

	if in_or_out == "out":
		return df['Artist IDs'].value_counts()

	if in_or_out == "in":
		return df['Related Artists IDs'].value_counts()

def combineEdgelists(edgeList1, edgeList2):
	# Takes two data frames and returns a combined dataframe

	Master_list = edgeList1.append(edgeList2,ignore_index=True)
	return Master_list.drop_duplicates()

def pandasToNetworkX(edgeList):
	# Takes an edge list and returns a directed graph

	g = nx.DiGraph()
	for Artist, Related_Artist in edgeList.to_records(index=False):
		g.add_edge(Artist,Related_Artist)


	return g

def randomCentralNode(inputDiGraph):

	node_dict = nx.eigenvector_centrality(inputDiGraph)
	norm_denominator = 0

	# Find sum of all values for denominator to normalize
	for node in node_dict:
		norm_denominator = norm_denominator + node_dict[node]

	# Normalize
	for node in node_dict:
		node_dict[node] = node_dict[node]/norm_denominator

	# Gets random node
	rndm_node = np.random.choice(node_dict.keys(),\
	p=node_dict.values())

	return rndm_node

# print(readEdgeList("Edge_Test.csv"))
# print degree(readEdgeList("Edge_Test.csv"),"in")
# print degree(readEdgeList("Edge_Test.csv"),"out")
# print combineEdgelists(readEdgeList("Edge_Test.csv"),\
# readEdgeList("Edge_Test2.csv"))
# pandasToNetworkX(readEdgeList("Edge_Test.csv"))
print randomCentralNode(pandasToNetworkX((readEdgeList("Edge_Test.csv"))))