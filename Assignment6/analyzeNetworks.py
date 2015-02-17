import requests
import pandas as pd

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

	Master_list = edgeList1.append(edgeList2, ignore_index=True)
	return Master_list.drop_duplicates()

# print(readEdgeList("Edge_Test.csv"))
# print degree(readEdgeList("Edge_Test.csv"),"in")
# print degree(readEdgeList("Edge_Test.csv"),"out")
print combineEdgelists(readEdgeList("Edge_Test.csv"),\
	readEdgeList("Edge_Test2.csv"))
