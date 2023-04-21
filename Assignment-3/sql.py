import mysql.connector as mysql
from my_tables import members, orders, cart
from datetime import datetime, timedelta

# if you dont have default setting on your database, change the following according to your settings
db = mysql.connect(user='root', password='root', port='8889', host='127.0.0.1', database='book_store')
mycursor = db.cursor(prepared=True)


# takes the members module from my_tabale and creates a new user in database
def create_new_user(members):

    query = "INSERT INTO members (fname, lname, address, city, state, zip, phone, email, password )\
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    mycursor.execute(query, (members.get_fname(),members.get_lname(),  members.get_address(),\
        members.get_city(),members.get_state() ,members.get_zip(),members.get_phone(),\
            members.get_email(), members.get_password()))

    db.commit()
    return members

# email is uniqe, checks if email is alredy taken when user creates a new account
def check_email(email):
    query = "SELECT COUNT(*) FROM members WHERE email = ?"
    mycursor.execute(query, (email,))
    result = mycursor.fetchone()
    return result[0] > 0

## fetches the user credentials from members
def show_user(email):

    query = "SELECT email, password, userid from members WHERE email = ?"
    mycursor.execute(query, (email,))
    rs = mycursor.fetchone()

    if rs is not None:
        members.set_email(rs[0])
        members.set_password(rs[1])
        members.set_userid(rs[2])  

        return members
    
    else:
        return None

# fetches the necessary information about user with given userid
def user_details(userid):
    query = "SELECT fname, lname, address, city, state, zip FROM members WHERE userid =?"
    mycursor.execute(query, (userid,))
    rs = mycursor.fetchone()

    if rs is not None:
        members.set_fname(rs[0])
        members.set_lname(rs[1])
        members.set_address(rs[2])
        members.set_city(rs[3])
        members.set_state(rs[4])
        members.set_zip(rs[5])
        return rs

    else: return None


#fetches subject, and returns it as a list
def fetch_subjects():
    query = 'SELECT subject FROM books GROUP BY subject'

    mycursor.execute(query)
    rs = mycursor.fetchall()
    subject_list = []
    for i in rs:
        subject_list.append(i[0])

    return subject_list

# takes subject as an argument, and fetches the all book details under the subject
def fetch_book_by_subject(subject):
    query = "SELECT * FROM books WHERE subject = ?"
    mycursor.execute(query, (subject,))
    rs = mycursor.fetchall()
    books = []
    
    for i in rs:
        book = (i[0], i[1], i[2], i[3], i[4])
        books.append(book)
    return books

# takes all information in cart module in my_table and inserts it in cart table
# Updates the quantity of wanted books if same isbn is eneterd
def save_to_cart(cart):
    query = "INSERT INTO cart (userid, isbn, qty) VALUES (?, ?, ?)\
        ON DUPLICATE KEY UPDATE qty = VALUES(qty)"

    mycursor.execute(query,(cart.get_userid(), cart.get_isbn(), cart.get_qty()))

    db.commit()
    return cart

# Fetches books either by the title or author
def fetch_books(substring, value):
    query = f"SELECT * FROM books WHERE {value} LIKE ?"
    mycursor.execute(query, ('%{}%'.format(substring),))

    rs = mycursor.fetchall()
    books = []

    for i in rs:
        book = (i[0], i[1], i[2], i[3], i[4])
        books.append(book)
    return books

# Fetches the cart contents of a user
def fetch_books_in_cart(userid):
    query = "select cart.isbn, cart.qty, books.title, books.price from cart\
            inner join members on members.userid = cart.userid\
            inner join books on books.isbn = cart.isbn\
            where cart.userid = ?"
    mycursor.execute(query, (userid,))

    rs = mycursor.fetchall()
    cart_list = []

    for i in rs:
        shoping = (i[0], i[1], i[2], i[3])
        cart_list.append(shoping)
    
    return cart_list

#Saves necessary information i order table 
def save_order(userid):
    date = datetime.now() + timedelta(days=7)
    date = date.strftime("%Y-%m-%d")

    query = "INSERT INTO orders (userid, received, shipAddress, shipCity, shipState, shipZip)\
        VALUES(?, ?, ?, ?, ?, ?)"

    mycursor.execute(query, (userid, date, members.get_address(), members.get_city(), members.get_state(), members.get_zip()))
    db.commit()

# fecthes contents from order table
def fectch_orders():
    query = "SELECT ono, received FROM orders WHERE ono = (SELECT MAX(ono) FROM orders)"
    mycursor.execute(query)
    
    rs = mycursor.fetchone()

    if  rs is not None:
        orders.set_ono(rs[0])
        orders.set_received(rs[1])
    return orders


# saves necessary content in odetails
def save_odetails(ono):
    query = "INSERT INTO odetails(ono, isbn, qty, price)\
            SELECT orders.ono, cart.isbn, cart.qty, (cart.qty*books.price) FROM orders\
            INNER JOIN cart ON cart.userid = orders.userid\
            INNER JOIN books ON books.isbn = cart.isbn\
            WHERE orders.ono = ?"


    mycursor.execute(query, (ono,))
    db.commit()

#empties the cart 
def empty_cart(userid):
    query = "DELETE FROM cart WHERE cart.userid = ?"

    mycursor.execute(query, (userid,))
    db.commit()

