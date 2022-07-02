###imports

#standard imports here
import csv
import os
import sys
from datetime import date
from datetime import datetime
import time
import gzip

os_path = os.path
csv_writer = csv.writer
sys_exit = sys.exit


###functions

def letter_replace(row):
    #many names (of people and films) have special characters in them. 
    #most can be handled by encoding the resulting files in ANSI, but some of them still pose an issue. 
    #here, i'm just replacing them so everything writes well.
    for i in range(len(row)):
        row[i] = row[i].replace("ā", "a").replace("ğ", "g").replace("ė", "e")
        row[i] = row[i].replace("ō", "o").replace("ē", "e").replace("ʽ", "'")
    return(row)

def avg_rating(title_list):
    #this is just so it's easy to find the average weighted rating of a group of films. 
    #only used to find 'imdb rating' for people, but could have other uses.
    weighted = 0
    samp = 0
    score = 999
    for i in title_list:
        try:
            weighted += (float(rating_dict[i][0][1]) * float(rating_dict[i][0][2]))
        except KeyError:
            weighted += 0
        try:
            samp += float(rating_dict[i][0][2])
        except KeyError:
            score = ''
        
    if score != '':
        score = weighted / samp
    
    return(score)

def gztsv_to_dict(file_name, inc_list, to_write, write_file):
    #this is what converts the raw imdb files into stored dictionaries. 
    #this takes the imdb file and a list of codes to include. 
    #it places rows into a dictionary, ignoring those that aren't in the 'inc_list'. 
    #no real processing is done here, this is just to slim down the csv files.
    #this also prints how long it took to process the file.
    dict_name = {}
    multi_row_list = []
    o_timestam = datetime.now()
    print(o_timestam)
    times = []
    with gzip.open(file_name, 'rt', encoding='utf-8') as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t', quotechar='\'', escapechar='|')
        for row in reader:
            if row[0] in inc_list:
                timestam = datetime.now()
                row = letter_replace(row)
                if row[0] not in multi_row_list:
                    dict_name[row[0]] = [row]
                    multi_row_list.append(row[0])
                else:
                    dict_name[row[0]].append(row)
                times.append(datetime.now() - timestam)
    
    if to_write == 'y':
        dict_to_csv(write_file, dict_name)
        
    
    print('max processing time: ', max(times))
    #print('min processing time: ', min(times))
    print('total processing time: ', datetime.now() - o_timestam)
    print(datetime.now())
    tsv_file.close()
    return (dict_name)

def dict_to_csv(file_name, dict_name):
    #this converts a dictionary to a new csv file. again, no processing.
    csv_file = open(file_name, 'w', newline='', encoding='ANSI')
    writer = csv_writer(csv_file, delimiter=',', quotechar=None,escapechar=' ')

    for key in dict_name:
        for i in range(0,len(dict_name[key])):
            writer.writerow(dict_name[key][i])
    csv_file.close()

###getting file names

watched_file_path = input('Input path to watched film .tsv or .tab file: ')
if not os_path.isfile(watched_file_path):
    print('file not found :(')
    sys_exit()

if not watched_file_path.endswith('.tsv') and watched_file_path.endswith('.tab'):
    print('you must input path to .tsv or .tab file')
    sys_exit()

#using default imdb names
titles = 'title.basics.tsv.gz'
principles = 'title.principals.tsv.gz'
crew = 'title.crew.tsv.gz'
names = 'name.basics.tsv.gz'
ratings = 'title.ratings.tsv.gz'

if not os_path.isfile(titles):
    print('titles file not found :(')
    sys_exit()
if not os_path.isfile(principles):
    print('principles file not found :(')
    sys_exit()
if not os_path.isfile(crew):
    print('crew file not found :(')
    sys_exit()
if not os_path.isfile(names):
    print('names file not found :(')
    sys_exit()
if not os_path.isfile(ratings):
    print('ratings file not found :(')
    sys_exit()

#creating names for cut files, if they get created
cut_titles = 'cut_titles.csv'
cut_principles = 'cut_principles.csv'
cut_crew = 'cut_crew.csv'
cut_names = 'cut_names.csv'
cut_ratings = 'cut_ratings.csv'

##determining what the user wants
#avoid retyping
wrong_letter = ('you must enter y or n')

#default can skip rest, if not the default then have to go deeper
default = input('do you want default settings [~produce all cut files, official vertex names] (y/n): ').lower()
if default == 'y':
    all_check_in = 'y'
elif default not in ('y','n'):
    print(wrong_letter)
    sys_exit()
else:
    all_check_in = input('do you want all the cut files? yes, some, or none?(y/s/n): ').lower()

#can skip selecting which files to produce, but can also choose specifics
if all_check_in in ('y','n'):
    title_check = all_check_in
    principles_check = all_check_in
    crew_check = all_check_in
    name_check = all_check_in
    rating_check = all_check_in

elif all_check_in == 's':

    title_check = input('do you want a cut title basics file? (y/n): ').lower()
    if title_check not in ('y', 'n'):
        print(wrong_letter)
        sys_exit()

    principles_check = input('do you want a cut title principles file? (y/n): ').lower()
    if principles_check not in ('y', 'n'):
        print(wrong_letter)
        sys_exit()
    crew_check = input('do you want a cut title crew file? (y/n): ').lower()
    if crew_check not in ('y', 'n'):
        print('you must enter y or n')
        sys_exit()

    name_check = input('do you want a cut name basics file? (y/n): ').lower()
    if name_check not in ('y', 'n'):
        print(wrong_letter)
        sys_exit()

    rating_check = input('do you want a cut title ratings file? (y/n): ').lower()
    if rating_check not in ('y', 'n'):
        print(wrong_letter)
        sys_exit()

else:
    print('you must enter y, s, or n')
    sys_exit


#asking if the vertex names (used for the plot) should be the official primary titles (with year) or the ones in the custom file. this should probably be the official unless every one of your titles is unique (or if the you don't want the english titles).
if default == 'y':
    name_op = 'o'
else:
    name_op = input("do you want the vertex (film titles) names to be imdb's official titles or yours? (o/y): ").lower()
    if name_op not in ('o', 'y'):
        print('you must enter o or y')
        sys_exit()


###actual processing

#start with custom file
watched_dict = {}
watched_codes = []
rating_list = []
o_timestam = datetime.now()
print(o_timestam)
with open(watched_file_path, 'r', newline='') as watched_tsv_file:

    reader = csv.reader(watched_tsv_file, delimiter='\t', quotechar='\'')
    next(reader)

    for row in reader:
        
        code = row[0]
        watched_date = datetime.strptime(row[1], '%m/%d/%Y')
        watched_date = datetime.date(watched_date)
        title = row[2]
        seen = row[3]
        source = row[4]
        recc = row[5]
        rating = row[6]
        simple = row[7]
        
        if code != 'NA':
            watched_codes.append(code)
            rating_list.append(code)
        
        watched_dict[code] = [code, watched_date, title, seen, source, recc, rating, simple]
        
#done with this
print(datetime.now())
print('collected watched films. time: ', datetime.now() - o_timestam)
watched_tsv_file.close()

#three files can be 'processed' now, the others need more info from these three
title_dict = gztsv_to_dict(titles, watched_codes, title_check, cut_titles)
print('titles done')
principle_dict = gztsv_to_dict(principles, watched_codes, principles_check, cut_principles)
print('principles done')
crew_dict = gztsv_to_dict(crew, watched_codes, crew_check, cut_crew)
print('crew done')

#getting all the people codes from priciples and crew (and tying them to their film).
people_codes = []
connection_list = []
for code in principle_dict:
    for i in range(0,len(principle_dict[code])):
        person = principle_dict[code][i][2]
        job = principle_dict[code][i][3]
        cat = principle_dict[code][i][4]
        if job != "\\N":
            role = job
        else:
            role = cat
    
        role = principle_dict[code][i][3]
        connection = [code, person, role]
        if connection not in connection_list:
            connection_list.append(connection)
        people_codes.append(person)

for code in crew_dict:
    directors = crew_dict[code][0][1]
    writers = crew_dict[code][0][2]
    dir_list = directors.split(',')
    wri_list = writers.split(',')
    for person in dir_list:
        connection = [code, person, 'director']
        if connection not in connection_list:
            connection_list.append(connection)
        if person not in people_codes:
            people_codes.append(person)
    for person in dir_list:
        connection = [code, person, 'writer']
        if connection not in connection_list:
            connection_list.append(connection)
        if person not in people_codes:
            people_codes.append(person)


people_dict = gztsv_to_dict(names, people_codes, name_check, cut_names)
print('names done')
   

#getting the known films for the people so they can be used in the average 'imdb' rating for each person
for person in people_dict:
    films = (people_dict[person][0][5]).split(',')
    for code in films:
        rating_list.append(code)
        
#final imdb file 'processing'
rating_dict = gztsv_to_dict(ratings, rating_list, rating_check, cut_ratings)
print('ratings done')


#this creates a dictionary of films, including the needed processing. 
#this is essentially what's included in the vertex file. 
#processing includes adding year to title names (for unique-ness) and breaking out the genres into three columns.
film_details = {}
for code in watched_codes:
    title = watched_dict[code][2]
    official = title_dict[code][0][2] + '(' + title_dict[code][0][5] + ')'
    watched = watched_dict[code][1]
    ttype = title_dict[code][0][1]
    year = int(title_dict[code][0][5])
    decade = year//10 * 10
    half_decade = (((year - decade) // 5) * 5) + decade
    age = (date.today().year - year)
    runtime = int(title_dict[code][0][7])
    genres = title_dict[code][0][8].split(',')
    genres.extend(['',''])
    genre1 = genres[0]
    genre2 = genres[1]
    genre3 = genres[2]
    seen = watched_dict[code][3]
    source = watched_dict[code][4]
    simple = float(watched_dict[code][7])
    imdb_rating = rating_dict[code][0][1]
    recc = watched_dict[code][5]
    film_details[code] = [code,
                          title,official,watched,ttype,year,
                          decade,half_decade,age,runtime,genre1,
                          genre2,genre3,seen,source,simple,
                          imdb_rating,recc]
#this does the same as above, but for people. 
people_details = {}
for code in people_codes:
    name = people_dict[code][0][1]
    official = people_dict[code][0][1] + '(' + code[-4:] + ')'
    watched = ''
    profs = (people_dict[code][0][4]).split(',')
    profs.extend(['','',''])
    ttype = profs[0]
    try:
        year = int(people_dict[code][0][2])
        decade = year//10 * 10
        half_decade = (((year - decade) // 5) * 5) + decade
        age = (date.today().year - year)
    except:
        year = ''
        decade = ''
        half_decade = ''
        age = ''
    runtime = ''
    prof1 = profs[0]
    prof2 = profs[1]
    prof3 = profs[2]
    seen = ''
    source = ''
    simple = ''
    imdb_rating = avg_rating((people_dict[code][0][5]).split())
    recc = ''
    people_details[code] = [code,
                          name,official,watched,ttype,year,
                          decade,half_decade,age,runtime,prof1,
                          prof2,prof3,seen,source,simple,
                          imdb_rating,recc]


#creating the edges and vertices files
print(datetime.now())
edges = open('edges.csv', 'w', newline='', encoding='ANSI')
writer = csv_writer(edges, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL,escapechar=' ')

writer.writerow(['title','name','role'])

for pair in connection_list:
    
    if connection_list[1] != '\\N':

        if name_op == 'o':
            i = 2
            k = (2,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)
            pk = (2,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)
        else:
            i = 1
            k = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)
            pk = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)

        pair[2] = pair[2].replace('"', "'")

        new_pair = [film_details[pair[0]][i],people_details[pair[1]][2],pair[2]]

        writer.writerow(new_pair)

print(datetime.now())
edges.close()


vert = open('vertices.csv', 'w', newline='', encoding='ANSI')
writer = csv_writer(vert, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL,escapechar=' ')

writer.writerow(['official_title','your_title','watch_date','type','year','decade','half_decade','age','runtime','genre1','genre2','genre3','seen','source','rating','imdb_rating','recommender'])

for key in film_details:
    film_row = []
    for thing in k:
        film_row.append(film_details[key][thing])
    writer.writerow(film_row)

for key in people_details:
    person_row = []
    for thing in pk:
        person_row.append(people_details[key][thing])
    writer.writerow(person_row)

print(datetime.now())
print('all done ...')
vert.close()