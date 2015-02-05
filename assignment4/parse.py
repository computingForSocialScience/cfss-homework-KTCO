import csv
import sys
import matplotlib.pyplot as plt

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

def zip_code_barchart():
	zip_dict={}
	permits = readCSV("permits_hydepark.csv")
	for j in range(len(permits)):
		current=permits[j]
		for i in range(28,len(current),7):
			cut=current[i]
			if cut=="":
				continue
			if cut[0:5] in zip_dict:
				zip_dict[cut[0:5]]+= 1
			else:
				zip_dict[cut[0:5]] = 1
	plt.bar(range(len(zip_dict)), zip_dict.values(), align='center')
	plt.xticks(range(len(zip_dict)), zip_dict.keys())
	plt.xticks(rotation=90)
	plt.savefig('BarChart.jpg')
if len(sys.argv)==1 or len(sys.argv)>2:
	sys.exit()
else:
	if sys.argv[1]=="latlong":
		get_avg_latlng()
	elif sys.argv[1]=="hist":
		zip_code_barchart()