import csv
import sys

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)


### enter your code below

def get_avg_latlng():
	'''Computes average latitude and longitude of construction permits
	in Hyde Park and prints it to the console ''' 
	permit_list = readCSV("permits_hydepark.csv")
	lat = 0
	lon = 0
	for i in range(len(permit_list)):
		list_item = permit_list[i]
		coordinates = list_item[-1]
		lat = lat+float(coordinates[1:17])
		lon = lon+float(coordinates[21:37])
	lat_avg = lat/len(permit_list)
	lon_avg = lon/len(permit_list)
	print "Avg latitude:",lat_avg,"Avg longitude:",lon_avg

# get_avg_latlng()

def zip_code_barchart():
	zip_dict={}
	permits = readCSV("permits_hydepark.csv")
	for j in range(len(permits)):
		current=permits[j]
		for i in range(28,len(current),7):
			if current[i]=="":
				continue
			if current[i] in zip_dict:
				zip_dict[current[i]] += 1
			else:
				zip_dict[current[i]] = 1
	print(zip_dict)

# zip_code_barchart()


