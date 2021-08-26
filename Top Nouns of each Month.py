import sqlite3, operator
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer #library that analyzes sentimental value of words

conn = sqlite3.connect("Nouns.db") #Pulls information from a Nouns SQL database 
cur = conn.cursor()

sid = SentimentIntensityAnalyzer() #command to pull the sentimantal analyzer out of the library

positive_words = {}
negative_words = {}

def delete_data(): #Script runs at the begining of the month. It drops the table after the script is ran.
    cur.execute("DROP TABLE Noun_Counter")
    cur.execute("CREATE TABLE Noun_incriments (ID INTEGER PRIMARY KEY AUTOINCREMENT, Date TEXT, Nouns TEXT, Occurences INT); ")
    conn.commit()

def sentiment_data(): #This goes into the words from the Noun_Counter database and analyzes each word to see if it seems positive or negative
    words_data = (cur.execute("SELECT * FROM Noun_Counter")).fetchall() #Turns the data into a dictionary
    month_data_stored = words_data[0][0] #Gets the month the data was stored in
    for word_info in word_data:
        if (sid.polarity_scores(i[1])['compound']) >= 0.5:
            positive_words[i[1]] = i[2] #If the value is above .5, it will be a positive word and stores it into a dictionary
        elif (sid.polarity_scores(i[1])['compound']) <= -0.5:
            negative_words[i[1]] = i[2] #If this values is below -.5, it will be a negative word and stores it in ad ictionary
    positive_sorted_values = dict(sorted(positive_words.items(), key = operator.itemgetter(1), reverse = True)[:5]) #this gets the top 5 most mentioned words
    negative_sorted_values = dict(sorted(negative_words.items(), key = operator.itemgetter(1), reverse = True)[:5]) #this gets the top 5 most mentioned words
    try: #checks to see if a table os created, if not, it will create a new tableet
        cur.execute("CREATE TABLE Positive_Noun_words (ID INTEGER PRIMARY KEY AUTOINCREMENT, Date TEXT, Nouns, TEXT, Occurences INT)") 
        cur.execute("CREATE TABLE Negative_Noun_words (ID INTEGER PRIMARY KEY AUTOINCREMENT, Date TEXT, Nouns, TEXT, Occurences INT)")
        conn.commit()
    except sqlite3.OperationalError: #adds in the positive and negative values into an SQL database for the top 5 words used per month
        for positive_word in positive_sorted_values:
            cur.execute("INSERT INTO Positive_Noun_words ( date, Nouns, Occurences) VALES(?, ?, ?)", (month_data_stored, positive_word[0], positive_word[1]))

        for negative_word in negative_sorted_values:
            cur.execute("INSERT INTO Positive_Noun_words ( date, Nouns, Occurences) VALES(?, ?, ?)", (month_data_stored, negative_word[0], negative_word[1]))

def init_data(): #since the database is made from another script, I forgot to add in the Integer value into the occurences. This portion takes out the values, renames it into the same table except turns the occurences into an integer value
    try: 
        cur.execute("CREATE TABLE Noun_incriments (ID INTEGER PRIMARY KEY AUTOINCREMENT, Date TEXT, Nouns TEXT, Occurences INT); ")
        cur.execute("ALTER TABLE Noun_Counter RENAME TO temp")
        curexecute("CREATE TABLE Noun_Counter(ID INTEGER PRIMARY KEY, Date TEXXT, Nouns Text, Occurences, INT);")
        cur.eecute("INSERT INTO Noun_Counter(ID, Nouns, Occurences) SELECT Date, Nouns, OCcurences FROM temp")
        cur.execute("DROP TABLE temp")
    except sqlite3.OperationalError:
        check_date()
        cur.execute("ALTER TABLE Noun_Counter RENAME TO temp")
        curexecute("CREATE TABLE Noun_Counter(ID INTEGER PRIMARY KEY, Date TEXXT, Nouns Text, Occurences, INT);")
        cur.eecute("INSERT INTO Noun_Counter(ID, Nouns, Occurences) SELECT Date, Nouns, OCcurences FROM temp")
        cur.execute("DROP TABLE temp")
        #Analysis

init_data()
sentiment_data()
delete_data()
