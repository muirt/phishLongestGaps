import os
from bs4 import BeautifulSoup
import unicodedata


#only need to download the song list when new shows occur
downloadSongList = False
sortSongList = True


class songEntry:

    def __init__(self):
        self.name = ""
        self.gap = -1
        self.artist = ""

def remove_unicode(s):
    return unicodedata.normalize('NFKD', s).encode('ascii','ignore')


#everything is in a single page
if downloadSongList:
    os.system("curl http://phish.net/song/ > currentGap.html")

if sortSongList:
    soup = BeautifulSoup(open("currentGap.html"), "lxml")

    #full chart contained inside <tbody> tag
    tableBody = soup.find_all('tbody')

    #make a list to hold all of the song objects
    songList = []

    #each child of <tbody> tag is a <tr> tag containing one song
    for entry in tableBody[0].children:
        #make a new song object
        song = songEntry()

        #parse the <tr> tag
        subSoup = BeautifulSoup(str(entry), "lxml")

        #each column of the table is a <td> tag
        songs = subSoup.find_all('td')
        for column in songs:

            #the name of the song has a link '/song/<song name>/history'
            if "/history" in str(column):
                song.name = column.a.contents[0]
            #the gap column is the only column that is numeric
            if str(column.contents[0]).isdigit():
                song.gap = int(column.contents[0])
            #the artist column has a link 'origartist=Phish'
            if "origartist" in str(column):
                song.artist = column.a.contents[0]
        #add the song to the list
        songList.append(song)

    #sort the list by gap
    sorted_songs = sorted(songList, key=lambda x: x.gap, reverse=True)

    #make a text file to hold the results
    out_file = open("longestGap.txt", "w")

    #print phish originals
    for s in sorted_songs:
        if s.artist.lower() == "phish":
            #default gap value is -1, meaning song has never been played
            if s.gap > -1:
                out_file.write(remove_unicode(s.name) + ": " + str(s.gap) + " shows\n\n")

    #make a gap between the lists
    out_file.write("\n\n\n")

    #print covers
    for s in sorted_songs:
        if s.gap > -1:
            if s.artist.lower() != "phish":
                out_file.write(remove_unicode(s.name) + " (" + remove_unicode(s.artist) + "): " + str(s.gap) + " shows\n\n")

    #close output file
    out_file.close()

