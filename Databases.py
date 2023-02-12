import sqlite3

db = sqlite3.connect('ebookstore')

cursor = db.cursor()

# create table if it does not already exist
cursor.execute(''' CREATE TABLE IF NOT EXISTS books 
                (
                    id INT PRIMARY KEY,
                    Title VARCHAR(100) ,
                    Author VARCHAR(50),
                    Qty INT
                ) ''')

db.commit()

# Add list of books to books table
books_list = [(3001,'A Tale of Two Cities','Charles Dickens',30),(3002,'Harry Potter and the Philosphers Stone','J.K. Rowling',40),(3003,'The Lion, the Witch and the Wardrobe','C.S. Lewis',25),(3004,'The Lord of the Rings','J.R.R. Tolkien',37),(3005,'Alice in Wonderland','Lewis Carroll',12)]

# insert values if they do not exist already
cursor.executemany(''' INSERT OR IGNORE INTO books VALUES (?,?,?,?)''', books_list)
db.commit()

# function to return all rows in the table for testing purposes
def return_all_rows():
    print()
    cursor.execute('''SELECT id, Title, Author, Qty from books''')

    for row in cursor:

        print(f"id : {row[0]} Title : {row[1]} Author : {row[2]} Qty : {row[3]}")

# function to print user menu
def print_menu():

    print("--------------Book Store Menu--------------------")
    print()
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit")

# update menu
def update_menu():
    
    print()
    print("---select the field you want to update--")
    print("1. Title")
    print("2. Author")
    print("3. Quantity")
    print("0. Return to main menu")


# function to check if input is int
def check_if_int (input_string, error_string):

    variable = 0

    while True:
        try:
            variable = int(input(input_string))
            break
        except ValueError:
            print(error_string)

    return variable

# function to update field in parameter and output message
def update_field(field_string, field_name, id):

    cursor.execute(f''' UPDATE books SET {field_string} = ? WHERE id =?''', (field_name,id))        
    db.commit()

    print(f"Your book with id {id} has been updated with {field_string} {field_name}")

# Main program loop

while True:
    # print user menu
    print_menu()

    # declare variable so if wrong input there isn't an issue later on in the code
    menu_option = ''

    # ensure user inputs a number
    try:
        menu_option = int(input("Please choose a number:"))
    except ValueError:
        print("Please enter a number!")

    # insert a new book    
    if menu_option == 1:
        
        print("Please enter book details:")       

        # Get inputs from user
        title = input("Please enter book title: ")
        author = input("Please enter book author: ")

        # use function to check quantity is an int
        qty = check_if_int("Please enter book quantity: ","Please enter a number for quantity!")

        # insert into database but autogenerate id
        cursor.execute(''' INSERT INTO books values((SELECT MAX(id)+1 FROM books),?,?,?)''', (title, author, qty))        
        db.commit()

        print(f"Your book {title} has been added to the system")

    if menu_option == 2:

        while True:
            
            # use function to check id is an int
            id = check_if_int("Please enter book id for book you wish to update or 0 to return: ","Please enter a number for id!")

            # exit loop if zero
            if id == 0 : 
                break

            # check if id exists in table
            cursor.execute('''SELECT id FROM books WHERE id= ?''',(id,))
            result = cursor.fetchone()

            if result is not None:
                break
            else:
                print("id does not exist.  Please try again")
        
        # if user chooses zero go back to main menu
        if id != 0:
            # display update menu
            update_menu()

            # use function to check user_option is an int
            update_option = check_if_int("Please choose an option: ","Please enter a number between 0 and 3")
            
            if update_option == 1:
                
                title = input("Please enter book title: ")    

                # update field and output message
                update_field('title', title, id)

            if update_option == 2:

                author = input("Please enter book author: ")

                # update field and output message
                update_field('author', author, id)

            if update_option == 3:

                # use function to check quantity is an int
                qty = check_if_int("Please enter book quantity: ","Please enter a number for quantity!")

                # update field and output message
                update_field('qty', qty, id)

    if menu_option == 3:

        while True:
            # use function to check id is an int
            id = check_if_int("Please enter book id for book you wish to update or 0 to return: ","Please enter a number for id!")

            # exit loop if zero
            if id == 0 : 
                break
            
            # check if id exists in table
            cursor.execute('''SELECT id FROM books WHERE id= ?''',(id,))
            result = cursor.fetchone()

            if result is not None:
                break
            else:
                print("id does not exist.  Please try again")

        # Go back to main menu if user selects zero
        if id != 0:
            # get title before row is deleted
            cursor.execute(''' SELECT title FROM books WHERE id =?''', (id,))   
            result = cursor.fetchone()

            # delete title
            cursor.execute(''' DELETE FROM books WHERE id =?''', (id,))        
            db.commit()

            print(f"Your book {result[0]} has been deleted")

    if menu_option == 4:

        # user can enter name or author to search
        title_or_author = input("Please enter part of title or author to search for books or ALL for complete list:")

        if title_or_author.upper() == "ALL":
            return_all_rows()
        
        # checks if any results exist
        cursor.execute(''' SELECT COUNT(*) FROM books WHERE title LIKE ? OR author LIKE ? ''', ('%'+title_or_author+'%','%'+title_or_author+'%'))
        results = cursor.fetchone()
        
        # check if any results are returned
        if results[0] == 0:
            print(f"No results found for search string: {title_or_author}")
        else:
            # searches for name or author and outputs results and outputs them
            cursor.execute(''' SELECT id, title, author, qty FROM books WHERE title LIKE ? OR author LIKE ? ''', ('%'+title_or_author+'%','%'+title_or_author+'%'))

            for row in cursor:
                
                print("--------------------")
                print(f"id : {row[0]}")
                print(f"Title : {row[1]}")
                print(f"Author: {row[2]}")
                print(f"Quantity: {row[3]}")
                print("--------------------")
            
                

    if menu_option == 0:
        break

    if isinstance(menu_option, int) and menu_option > 4:
        print("Option does not exist.  Please choose between 0-4.\n")


db.close()
