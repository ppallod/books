import os
import requests
from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variables
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

if not os.getenv("KEY"):
    raise RuntimeError("Goodreads API KEY not set")

# GoodReads API
URL = "https://www.goodreads.com/book/review_counts.json"
KEY = os.getenv("KEY")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# User Class
class User():
    def __init__(self):
        self.user_id = None
        self.username = None
        self.password = None

# Initializing the Class
current_user = User()

@app.route("/")
def index():
    "See if User has Already Signed In"
    if current_user.username != None:
        return redirect(url_for('search'))
    else:
        return render_template("index.html")

@app.route("/logout")
def logout():
    
    current_user.username = None
    current_user.username = None
    current_user.user_id = None
    
    return redirect(url_for('index'))


@app.route("/signin", methods = ["POST"])
def signin():
    username = request.form.get("username")
    password = request.form.get("password")

    """Check if User Exists"""
    signin = db.execute("SELECT * FROM users WHERE username = :username AND password = :password ",{"username": username, "password": password}).fetchone()
    if signin is None:
        return render_template("error.html", message="Username or Password is Incorrect",link='index')
    
    #Adding Username for future reference
    current_user.username = signin.username
    current_user.user_id = int(signin.user_id)
    current_user.password = signin.password

    return render_template("search.html")

@app.route("/signup", methods = ["GET","POST"])
def signup():

    if request.method == "GET":
        return render_template("signup.html")

    username = request.form.get("username")
    password = request.form.get("password")

    """Check if Username already Exists"""
    exists = db.execute("SELECT * FROM users WHERE username = :username ",{"username": username}).fetchone()
    if exists != None:
        return render_template("error.html", message = "Username already exists. Please try another username", link="index")
    
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",{"username": username, "password": password})
    db.commit()

    return render_template("success.html", message = "You've Successfully SignedUp!. Please sign in to continue",link='index')

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")

    search_text = '%'+ request.form.get("search")+'%'
    books = db.execute("""SELECT * FROM books WHERE isbn ilike :search_text 
                        UNION ALL
                        SELECT * FROM books WHERE title ilike :search_text
                        UNION ALL
                        SELECT * FROM books WHERE author ilike :search_text
                        """,{"search_text": search_text}).fetchall()
    
    if len(books)==0:
        return render_template("error.html",message="Book not Found",link='search')
    
    return render_template("books.html",books=books)

@app.route("/reviews/<string:isbn>", methods=["GET","POST"])
def reviews(isbn):
    "Insert the Review INTO Database"

    if request.method=="POST":
        review = request.form.get("my_review")
        rating = int(request.form.get("rating"))
        db.execute("INSERT INTO reviews (user_id, isbn, rating, review) VALUES (:user_id, :isbn, :rating, :review)",{"user_id":current_user.user_id,"isbn":isbn,"rating":rating,"review":review})
        db.commit()
        return render_template("success.html",message="You have successfully added your review",link='reviews',isbn=isbn)


    """Get Details about the Book"""
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn;",{"isbn":isbn}).fetchone()
    print(book.isbn)
    data = requests.get(URL,params={"key":KEY,"isbns":book.isbn})
    rating_count = data.json()["books"][0]["work_ratings_count"]
    average_rating = data.json()["books"][0]["average_rating"]

    """Search if Reviews Already Exists"""
    reviews = db.execute("SELECT review, rating FROM reviews WHERE user_id = :user_id AND isbn = :isbn",{"user_id":current_user.user_id,"isbn":isbn}).fetchone()
    if reviews == None:
        review = None
        rating = None
    else:
        review = reviews.review
        rating = reviews.rating
    return render_template("reviews.html",book=book,rating_count=rating_count,average_rating=average_rating,review=review,rating=rating)

