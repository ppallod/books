import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

#Creating the DB Engine
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine)) 

#Reading Data From the CSV File
filename = open("books.csv")
reader = csv.reader(filename)
next(reader,None)

#Inserting Records into the Table
for isbn, title, author, year in reader:
    print("INSERT INTO books (isbn,title,author, year) VALUES (:isbn, :title, :author, :year)",{"isbn": isbn,"title":title, "author": author, "year": year})
    db.execute("INSERT INTO books (isbn,title,author, year) VALUES (:isbn, :title, :author, :year)",{"isbn": isbn,"title":title, "author": author, "year": year})

db.commit()