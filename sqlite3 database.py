from Praw_Counter import new_final_nouns #Gets the dictionary from the Noun Counter Script
import sqlite3, os
from collections import Counter
from datetime import datetime

Counter_Nouns = Counter()

conn = sqlite3.connect(r"nouns.db")#Connects to the a database
c = conn.cursor()

def Action():
    date = datetime.today().strftime("%b %Y") #Gets the date these values are processed
    for item, number in new_final_nouns:
        c.execute("INSERT INTO Noun_Counter VALUES (?, ? , ?)", (date,item, number)) #Adds the values into the SQL data base
    [c.execute("INSERT INTO Noun_Counter Values(?, ?, ?)", (date, item, number)) for item, number in Counter_Nouns.items()]
    conn.commit()
    conn.close()
    
try: #If the table is not created yet, this will create the table.
    c.execute('''CREATE TABLE Noun_Counter (Date, Nouns, Occurences)''')
    Action()
except sqlite3.OperationalError:
    Action()
print("done")

