#CS-50W Project 1
###MyBooks.Com

In this project, I have built a Webapplication for my Book Review website - MyBooks.com

* I have built a Flask Application (application.py) using Heroku Postgresql Database.
* On the Datbase side (Tables.sql), I've build three tables - Users, Books & Reviews.
    * Users -  contains the data about the existing users from my website. Once a new user registers on my application, their data would be stored in this table.
    * Books - stores the data about all the 5000 books from books.csv.
    * Reviews - stores the reviews data.
* I have used (import.py) for importing the books.csv data.
* All the html templates are contained in the folder - templates


####Requirements - 
* Apart from the requirements.txt for building the Python enviroment, the user needs to define Environment Variables - 'DATABASE_URL' & 'KEY'
    * DATABASE_URL - This is the Postgresql Server URL
    * KEY - GoodReads API KEY

