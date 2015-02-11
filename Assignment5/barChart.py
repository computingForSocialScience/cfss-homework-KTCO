import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
    f_artists = open('artists.csv') # opens file 'artists.csv' and assigns it to variable f_artits
    f_albums = open('albums.csv') # opens file 'albums.csv' and assigns it to variable f_albums

    artists_rows = csv.reader(f_artists) # reads f_artists and assigns it to variable artits_rows
    albums_rows = csv.reader(f_albums) # reads f_albums and assignes it to variable albums_rows

    artists_header = artists_rows.next()
    albums_header = albums_rows.next()

    artist_names = [] # creates empy list
    
    decades = range(1900,2020, 10) # creates a list of numbers from 1900 to 2020 in intervals of 10
    decade_dict = {} # Creates empty dictionary
    for decade in decades:  # fills dictionary with entries from decades and assigns a value of 0
        decade_dict[decade] = 0
    
    # loops through each row in artists rows and checks to see if current row is the same as the last one
    # If it isn't then it appends it to list artist_names

    for artist_row in artists_rows: 
        if not artist_row:
            continue
        artist_id,name,followers, popularity = artist_row
        artist_names.append(name)

    # Loops through each row in album_rows and checks to see if current row is the same as the last one
    # If it isn't then it checks the year of the current album and updates the dictionary to reflect an
    # additional album in a certain decade

    for album_row  in albums_rows:
        if not album_row:
            continue
        artist_id, album_id, album_name, year, popularity = album_row
        for decade in decades:
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)):
                decade_dict[decade] += 1
                break


    x_values = decades # assigns the list of decades from 1900 to 2020 to variable
    y_values = [decade_dict[d] for d in decades] # assigns the keys of dictionaries to variable y_values
    return x_values, y_values, artist_names # returns variables x_values, y_values, and artist_names

def plotBarChart():
    # calls function getBarChartData and assigns the returned values to variables x_vals, y_vals, and artist_names
    x_vals, y_vals, artist_names = getBarChartData()
    
    # creates and shows a plot using the variables from function getBarChartData
    # With the x axis being decades, y axis being the number of albums

    fig , ax = plt.subplots(1,1)
    ax.bar(x_vals, y_vals, width=10)
    ax.set_xlabel('decades')
    ax.set_ylabel('number of albums')
    ax.set_title('Totals for ' + ' | '.join(artist_names))
    plt.show()
