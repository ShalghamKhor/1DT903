import functions as fun
from sql import show_user, user_details
from my_tables import memberss

# Constants
MAIN_MENU = """
**************************************************
***      Welcome to Online Book Store          ***
***                                            ***
**************************************************
        1. Login                                 
        2. New Member Registration              
        q. Quit                                  
"""

MEMBER_MENU = """
**************************************************
***      Welcome to Online Book Store          ***
***              Member Menu                   ***
**************************************************
        1. Browse by subject                                
        2. Search by Author/Title
        3. Check Out              
        q. Quit                                  
"""

SEARCH_MENU = """
[1] Author search
[2] Title search
[3] Go Back to Member Menu
"""

# Program entry point
def main():
    while True:
        print(MAIN_MENU)
        choice = input("Enter your choice: ")

        if choice == '1':
            email = input("Enter your email: ")
            password = input("Enter your password: ")

            # Validate login credentials
            if validate_login(email, password):
                # Show member menu
                member_menu()
            else:
                print("Invalid login credentials")

        elif choice == '2':
            fun.createuser()

        elif choice.lower() == 'q':
            break

        else:
            print("Invalid input. Please try again.")

    print("Goodbye!")

# Validate member login
def validate_login(email, password):
    user = show_user(email)
    if user is None:
        return False
    elif user.get_password() == password:
        user_details(user.get_userid())
        return True
    else:
        return False

# Display member menu and handle user input
def member_menu():
    while True:
        print(MEMBER_MENU)
        choice = input("Enter your choice: ")

        if choice == '1':
            fun.show_subjects_and_books()

        elif choice == '2':
            search_engine()

        elif choice == '3':
            fun.checkout()

        elif choice.lower() == 'q':
            break

        else:
            print("Invalid input. Please try again.")

# Display search menu and handle user input
def search_engine():
    while True:
        print(SEARCH_MENU)
        choice = input("Enter your choice: ")

        if choice == '1':
            #fun.search_author()
            a = 'author'
            fun.search(a)

        elif choice == '2':
            #fun.search_title()
            a = "title"
            
            fun.search(a)
        elif choice == '3':
            break

        else:
            print("Invalid input. Please try again.")

if __name__ == '__main__':
    main()
