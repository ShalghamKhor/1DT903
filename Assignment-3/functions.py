from my_tables import members, cart, orders
from sql import create_new_user, fetch_books, fetch_subjects, fetch_book_by_subject\
    ,save_to_cart, fetch_books_in_cart, save_order, fectch_orders, \
    save_odetails, empty_cart, check_email

# creating new user
def createuser():
    print()
    print('press ENTER key to return menu\n')
    members.set_fname(input('enter your first name >> '))
    members.set_lname(input('enter your lastname >> '))
    members.set_address(input('enter your address >> '))
    members.set_city(input('enter your city >> '))
    members.set_state(input('Enter state >> '))
    members.set_zip(input('enter your zipcode >> '))
    members.set_phone(input('enter your phoner numer >> '))
    while True:
        email = input('enter your email >> ')
        if check_email(email):
            print("Email alredy taken !! ")
        else:
            members.set_email(email)
            password = input('enter your password >> ')
            members.set_password(password)
            break

    create_new_user(members)

# Display books by choosen subject
def show_subjects_and_books():

    subjects = fetch_subjects()
    n = 1
    for i in subjects:
        print(f'{n}.   {i}' )
        n +=1

    user_value = int(input("select a subject >> "))
    subject = subjects[user_value - 1]
    books = fetch_book_by_subject(subject)
    print(f'\n{len(books)} available on this subject')
    books_to_show = 0

    while books_to_show < len(books):
        print("-----------------------------------------------")
        book1 = books[books_to_show]
        print(f'{books_to_show+1}. \nAuthor: {book1[1]}\ntitle: {book1[2]}\nisbn: {book1[0]}\nprice: {round(book1[3],2)}\nsubject: {book1[4]}')
        books_to_show += 1

        if books_to_show < len(books):
            print("----------------------------------------------")
            book2 = books[books_to_show]
            print(f'{books_to_show+1}. \nAuthor: {book2[1]}\ntitle: {book2[2]}\nisbn: {book2[0]}\nprice: {round(book2[3],2)}\npsubject: {book2[4]}')
            books_to_show += 1

        while True:
            print("----------------------------------------------")
            next_2books = input("press 'n' to show more, press ENTER to go to Menu, ENTER isbn to add to cart >>  ")
            if next_2books.lower() == 'n':
                break
            if next_2books == '':
                books_to_show = len(books)
                break
            #else:
            elif any(next_2books == book[0] for book in books):
                cart.set_qty(input("Enter quatity >> "))
                cart.set_isbn(next_2books)
                cart.set_userid(members.get_userid())
                save_to_cart(cart)
                break
            else:
                print("Invalid input: ")

# displays 3 books at a time 
def search(val):
    input_ = input(f"Enter {val} or part of the {val}: ")
    books = fetch_books(input_, val)
    print(f'\n{len(books)}, books found')
    books_to_show = 0
    while books_to_show <len(books):
        print("----------------------------------------------")
        book1 = books[books_to_show]
        print(f'{books_to_show+1}. \nAuthor: {book1[1]}\ntitle: {book1[2]}\nisbn: {book1[0]}\nprice: {round(book1[3],2)}\nsubject: {book1[4]}')
        books_to_show += 1

        if books_to_show < len(books):
            print("----------------------------------------------")
            book2 = books[books_to_show]
            print(f'{books_to_show+1}. \nAuthor: {book2[1]}\ntitle: {book2[2]}\nisbn: {book2[0]}\nprice: {round(book2[3],2)}\nsubject: {book2[4]}')
            books_to_show += 1

        if books_to_show < len(books):
            print("----------------------------------------------")
            book3 = books[books_to_show]
            print(f'{books_to_show+1}. \nAuthor: {book3[1]}\ntitle: {book3[2]}\nisbn: {book3[0]}\nprice: {round(book3[3],2)}\nsubject: {book3[4]}')
            books_to_show += 1
        
        while True:
            print("----------------------------------------------")
            next_2books = input("press 'n' to show more, press ENTER to go to Menu, ENTER isbn to add to cart >>  ")
            if next_2books.lower() == 'n':
                break

            if next_2books == '':
                books_to_show = len(books)
                break

            elif any(next_2books == book[0] for book in books):
                cart.set_qty(input("Enter quatity >> "))
                cart.set_isbn(next_2books)
                cart.set_userid(members.get_userid())
                save_to_cart(cart)
                break

            else:
                print("Invalid input: ")

# Dsiplays users cart content
def checkout():
    loop = True
    shop = fetch_books_in_cart(members.get_userid())
    
    if len(shop) != 0:
        max_title_lengt = max(len(i[2]) for i in shop)
        contents = ("{:<10} {:<{width}} {:<8} {:<5} {:<10}".format('ISBN', 'Title', '$', 'Qty', 'Total', width=max_title_lengt))
        total = 0
        print("Current cart content\n ")
        print(contents)
        print("-" * (max_title_lengt + 33))

        for i in shop:
            print(f"{i[0]:<10} {i[2]:<{max_title_lengt}} {i[3]:<8.2f} {i[1]:<5} {i[1]*i[3]:<10.2f}")
            print("-" * (max_title_lengt + 33))
            total += i[1]*i[3]

        print(f"{'Total =':<{max_title_lengt +25}} ${total:<0.2f}")
        print("-" * (max_title_lengt + 33))

        while loop:
            inpu_ = input("proceed to checkout (Y/N)? >> ")

            if inpu_.lower() == 'y':
                orders.set_total(total)
                invoice()
                loop = False
            if inpu_.lower() == 'n':
                loop = False
            else: print('Invalid Input!')

    else: print("your shopping cart is empty")

# Dsiplays the invoice for the ordernummer, empties contents in a cart
def invoice():
    save_order(members.get_userid())
    fectch_orders()
    save_odetails(orders.get_ono())
    shop = fetch_books_in_cart(members.get_userid())
    
    if len(shop) != 0:
        max_title_lengt = max(len(i[2]) for i in shop)
        contents = ("{:<10} {:<{width}} {:<8} {:<5} {:<10}".format('ISBN', 'Title', '$', 'Qty', 'Total', width=max_title_lengt))
        total = 0
        print()
        print(f"{'':<{len(contents)/2}} Invoice for Order No.{orders.get_ono()}")
        print()
        print(f"{'':<{len(contents)/10}} Shipping address {'':<{len(contents)/5}} Billing Address")
        print(f"{'':<{len(contents)/10}} Name:  {members.get_fname()} {members.get_lname():<{len(contents)/4}} Name:   {members.get_fname()} {members.get_lname()}")
        print(f"{'':<{len(contents)/10}} Address:  {members.get_address():<{len(contents)/4}} Address:  {members.get_address()}")
        print(f"{'':<{len(contents)/5}}{members.get_city():<{len(contents)/3}} {members.get_city()}")
        print(f"{'':<{len(contents)/5}}{members.get_state():<{len(contents)/3}} {members.get_state()}\n ")
        print(f"{'':<{len(contents)/3}} Estimate delivery Date {orders.get_received()}")
        
        print(contents)
        print("-" * (max_title_lengt + 34))

        for i in shop:
            print(f"{i[0]:<10} {i[2]:<{max_title_lengt}} {i[3]:<8.2f} {i[1]:<5} {i[1]*i[3]:<10.2f}")
            print("-" * (max_title_lengt + 34))
            total += i[1]*i[3]

        print(f"{'Total =':<{max_title_lengt +27}} ${total:<10.2f}")
        print("-" * (max_title_lengt + 34))
        loop = True
        while loop:
            inpu_ = input("Press ENTER to go to Menu >> ")

            if inpu_.lower() != '':
                print("Enter a valid Key")
            else:
                empty_cart(members.get_userid())
                loop = False
