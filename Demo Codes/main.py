import csv
from datetime import datetime, timedelta
#This function is used to link the csv with the python file. by doing this, the tables created in the csv files can be read
# The import date time is used to enable the use of dates within the codes as this will be necessary in other menu systems.
# Login system Menu is created to allow user to access the database. With this function, user can input the username and the password.

def login_system():
    """Handles user login."""
    USERNAME = "f"
    PASSWORD = "f"
# the while loop ensures that user will not be able to go to the next step if the username of passowerd is left empty.
# using the strip() function, the code is used to remove any white space from the input and if there is no value after that, the user will be prompted 
#to enter the correct a value
    while True:
        username = input("Enter username: ").strip().lower()
        if not username:
            print("Username cannot be empty. Please try again.")
            continue

        password = input("Enter your password: ").strip().lower()
        if not password:
            print("Password cannot be empty. Please try again.")
            continue

        if username == USERNAME and password == PASSWORD:
            print("Login successfully")
            break
        else:
            print("Login failed. Please try again")



#This section checks if the csv files exist and if it dosent, it shows an error for file not found. to read the csv file, it uses the mode 'r'
# Read CSV file
def read_csv(file_name):
    try:
        with open(file_name, mode='r') as file:
            rows = list(csv.reader(file))
            if not rows:
                raise ValueError(f"{file_name} is empty.")
            return rows
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
        return []
    except ValueError as e:
        print(e)
        return []
#This is used to edit the the csv file wehre necessary it opens the CSV file and then writes information when necessary. the mode to do this is mode 'w'
# Write to CSV file
def write_csv(file_name, data, header):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
#This is the first option in the menu system. it is basically used to display all the list of the books and the information available.

# View list of books
def view_books():
#Display the list of books and their availability
    books = read_csv('Books.csv')
    if len(books) <= 1:
        print("No books available in the library.")
        return
    print("\n--- List of Books ---")
    for row in books[1:]:
        if len(row) < 8:
            print("Incomplete book record found. Skipping...")
            continue
        print(f"Book ID: {row[0]}, ISBN: {row[1]}, Title: {row[2]}, Author: {row[3]}, "
              f"Publisher: {row[4]}, Pages: {row[5]}, Available: {row[6]}, Copies Available: {row[7]}") #This is used to identifies all the rows in the tables each row is counted from 0 to the last number.
#
#The same is being done to view the list of students as with the books.
# View list of students
def view_students():
    """Display the list of students."""
    students = read_csv('Students.csv')
    if len(students) <= 1:
        print("No students registered.")
        return
    print("\n--- List of Students ---")
    for row in students[1:]:
        if len(row) < 5:
            print("Incomplete student record found. Skipping...")
            continue
        print(f"Student ID: {row[0]}, Name: {row[1]}, Badge Number: {row[2]}, Contact: {row[3]}, Course: {row[4]}") #It also arranges them in the right order and displays them

# To lend a book, this functon allows user to update the borrowing.csv from the students.csv and Books.csv. It should also change the number of copies and update whether the book is available or not
# Lend a book
def lend_book():
#Lend a book to a student
    book_id = input("Enter Book ID: ")
    student_id = input("Enter Student ID: ")

    books = read_csv('Books.csv')
    students = read_csv('Students.csv')
    borrowings = read_csv('Borrowings.csv')

    time = int(input("Enter the number of days: ")) #This is for the number of day that the book should be borrowed.

    if not any(len(row) >= 8 and row[0] == book_id for row in books[1:]): #This is to check that the book.csv file is suppose to have the required number or rows in the file if not the error will be displayed.
        print(f"Error: Book ID {book_id} not found.")
        return

    if not any(len(row) >= 5 and row[0] == student_id for row in students[1:]):# This does the same for that of the book ID
        print(f"Error: Student ID {student_id} not found.")
        return


    # This will be used to Get book and student details
    book_row = next(row for row in books[1:] if len(row) >= 8 and row[0] == book_id) #this used to also check that the length of the book in the csv file exist and is as it should be with the bookid being the first name
    student_row = next(row for row in students[1:] if len(row) >= 5 and row[0] == student_id)# the same for the student table

    if book_row[6].lower() == 'true' and int(book_row[7]) > 0:
        if any(len(borrow) >= 4 and borrow[0] == student_id and borrow[3] == book_id for borrow in borrowings[1:]):
            print(f"Student ID {student_id} has already borrowed Book ID {book_id}.")
            return

        book_row[7] = str(int(book_row[7]) - 1) #This is used to Reduce the number of available copies [7] with the book table and when it goes to 0, the available status should change to False from True.
        if int(book_row[7]) == 0:
            book_row[6] = 'False'
# The dates are then being arranged here to show the calculation based on the input of the user for how many days the book shoulb be lended
        due_date = (datetime.now() + timedelta(days=time)).strftime('%Y-%m-%d') 
        borrowings.append([
            student_id, student_row[1], student_row[2], book_id, book_row[2],
            datetime.now().strftime('%Y-%m-%d'), due_date
        ])
        write_csv('Borrowings.csv', borrowings[1:], borrowings[0])
        write_csv('Books.csv', books[1:], books[0])
        print(f"Book {book_id} has been lent to Student ID {student_id}. Due on {due_date}.")
    else:
        print(f"Book ID {book_id} is not available.")

#The Function is used to return book that is recorded in the borrowing table. To return book here, the user must input the student id and the book id and then the data is is being read to edit the information
# Return a book
def return_book():
    """Return a borrowed book."""
    book_id = input("Enter Book ID: ")
    student_id = input("Enter Student ID: ")# this is to input the date for both the book and the student id

    borrowings = read_csv('Borrowings.csv')
    books = read_csv('Books.csv')

    for row in borrowings[1:]:
        if len(row) >= 7 and row[0] == student_id and row[3] == book_id:#This is used to check the length values of the borrowings.csv fiel if it matches the input, the data is  removed
            borrowings.remove(row)

            for book_row in books[1:]:#This used to skip the heading and it is used in varoius sections of the code
                if len(book_row) >= 8 and book_row[0] == book_id:
                    book_row[7] = str(int(book_row[7]) + 1) #This add the number of copies into the book id
                    if int(book_row[7]) > 0:
                        book_row[6] = 'True'# if necessary, it also turns the false to true

            due_date = datetime.strptime(row[6], '%Y-%m-%d') #With the date time function, the return date is being calculated
            return_date = datetime.now()
            fine = max(0, (return_date - due_date).days * 2) #The fine is for the boooks that is borrowed and have not been returned. It is £2 for each day after the due date.

            write_csv('Books.csv', books[1:], books[0])
            write_csv('Borrowings.csv', borrowings[1:], borrowings[0])
            print(f"Book {book_id} returned successfully.")
            if fine > 0:
                print(f"Late return fine: £{fine}.")
            else:
                print("Balance = £0.")
            return

    print(f"Borrowing record not found for Book ID {book_id} and Student ID {student_id}.")

# View books borrowed by a student is used to show the list of book that a student have borrowed. With this, all that is needed is the students id and the rest will show in the code.
def view_books_borrowed_by_student():
# View books borrowed by a specific student
    student_id = input("Enter Student ID: ")
    borrowings = read_csv('Borrowings.csv')

    print(f"\n--- Books Borrowed by Student {student_id} ---")
    for row in borrowings[1:]:
        if len(row) >= 7 and row[0] == student_id: #This is to confirm that the file exist and that it is  in the right order
            print(f"Student ID: {row[0]}, Name: {row[1]}, Badge Number: {row[2]}, "
                  f"Book ID: {row[3]}, Title: {row[4]}, Lending Date: {row[5]}, Due Date: {row[6]}")
#This function is used to add new book and update the amount of copies that are already in a existing book
# Add a new book
def add_new_book():
    """Add a new book or copies of an existing book."""
    books = read_csv('Books.csv')

    while True:  # Loop to ensure valid input
        print("1. Add copies to an existing book")
        print("2. Add a new book")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':  # Add copies to an existing book
            book_id = input("Enter Book ID to add copies: ")
            if not any(len(row) >= 8 and row[0] == book_id for row in books[1:]):#This checks if row exist in the book.csv file and ensures that it has at least 8 columns.
                print(f"Book ID {book_id} not found.")
                return
            try:
                copies_to_add = int(input("Enter number of copies to add: "))
                for row in books[1:]:
                    if len(row) >= 8 and row[0] == book_id:
                        row[7] = str(int(row[7]) + copies_to_add) #This shows how the copies are being updated and added into the system.
                        row[6] = 'True'
                write_csv('Books.csv', books[1:], books[0])
                print(f"{copies_to_add} copies added to Book ID {book_id}.")
            except ValueError:
                print("Error: Please enter a valid number for copies.")
            break  # Exit loop after completing operation

        elif choice == '2':  # Add a new book
            book_id = input("Enter Book ID: ")# these are all the input statements for second choice
            isbn = input("Enter ISBN: ")
            title = input("Enter Book Title: ")
            author = input("Enter Book Author: ")
            publisher = input("Enter Publisher: ")
            pages = input("Enter Number of Pages: ")
            copies_available = input("Enter Copies Available: ")

            #This Ensures that the numeric fields are integers
            if not book_id.isdigit() or not isbn.isdigit() or not pages.isdigit() or not copies_available.isdigit():
                print("Error: Book ID, ISBN, Pages, and Copies Available must be integers.")
                return

            # Check for duplicates values within the code.
            if any(len(row) >= 8 and (row[0] == book_id or row[1] == isbn) for row in books[1:]):
                print("Error: Book ID or ISBN already exists.")
                return

            availability = 'True' if int(copies_available) > 0 else 'False'
            books.append([book_id, isbn, title, author, publisher, pages, availability, copies_available])
            write_csv('Books.csv', books[1:], books[0])
            print(f"New book '{title}' added successfully.")
            break  # Exit loop after completing operation is successful 

        else:
            print("Error: Please select between 1 and 2.")  # Invalid input, loop continues

# Delete a book will have two options one for deleting a book or deletig a copy of a book that alaready exist.
def delete_book():
#Delete a book or copies from the library
    book_id = input("Enter Book ID to delete: ")
    books = read_csv('Books.csv')

    if not any(len(row) >= 8 and row[0] == book_id for row in books[1:]):
        print(f"Book ID {book_id} not found.")
        return

    while True:  # Loop to repeatedly ask for valid input
        print("1. Delete entire book entry")
        print("2. Delete specific copies")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            books = [row for row in books if len(row) < 8 or row[0] != book_id]
            write_csv('Books.csv', books[1:], books[0])
            print(f"Book ID {book_id} deleted successfully.")
            break  # Exit the loop after successful deletion
        elif choice == '2':
            copies_to_delete = int(input("Enter number of copies to delete: "))
            for row in books[1:]:
                if len(row) >= 8 and row[0] == book_id:
                    if copies_to_delete > int(row[7]):
                        print("Error: Cannot delete more copies than available.")
                        return
                    else:
                        row[7] = str(int(row[7]) - copies_to_delete)
                        if int(row[7]) == 0:
                            row[6] = 'False'
                    break
            write_csv('Books.csv', books[1:], books[0])
            print(f"{copies_to_delete} copies of Book ID {book_id} deleted successfully.")
            break  # Exit the loop after successful deletion
        else:
            print("Error: Please select between 1 and 2.")  # Invalid input, loop continues

# Add a new student Works just like add book. the only difference is the not having options to add book copies.
def add_new_student():
# Add a new student to the library system
    student_id = input("Enter Student ID: ")
    student_name = input("Enter Student Name: ")
    badge_number = input("Enter Badge Number: ")
    contact = input("Enter Contact Number: ")
    course = input("Enter Course: ")

    if not student_id.isdigit()  or not contact.isdigit(): #or not badge_number.isdigit()
        print("Error: Student ID,  and Contact must be integers.") #Badge Number,
        return

    students = read_csv('Students.csv')
    if any(len(row) >= 5 and (row[0] == student_id or row[2] == badge_number or row[3] == contact) for row in students[1:]):
        print("Error: Duplicate Student ID, Badge Number, or Contact.")
        return

    students.append([student_id, student_name, badge_number, contact, course])
    write_csv('Students.csv', students[1:], students[0]) 
    print(f"New student '{student_name}' added successfully.")


# Delete a student
def delete_student():
# Delete a student from the library system
    student_id = input("Enter Student ID to delete: ")

    students = read_csv('Students.csv')
    if not any(len(row) >= 5 and row[0] == student_id for row in students[1:]):
        print(f"Student ID {student_id} not found.")
        return

    while True:  # Loop to repeatedly ask for valid confirmation
        confirm = input("Are you sure you want to delete this student? (y/n): ").lower()
        if confirm == 'y':
            for row in students[1:]:
                if len(row) >= 5 and row[0] == student_id:
                    students.remove(row)
                    write_csv('Students.csv', students[1:], students[0])
                    print(f"Student ID {student_id} has been deleted successfully.")
                    return
        elif confirm == 'n':
            print("Operation cancelled. No student was deleted.")
            return
        else:
            print("Error: Please enter 'y' for yes or 'n' for no.")  # Invalid input, loop continues


# The Main function is what is being used to show the menu system and the options. Within this options there are various loop 
# that have been made to make sure that the user intput is woring fine.

def main():
    """Main function to run the library management system."""
    print("Welcome to Adamstown Library Management System!")
    login_system()

    while True:
        name_input = input("Please Enter Your First Name: ").strip().upper()
        if not name_input:
            print("Name cannot be empty. Please enter a valid name.")
        else:
            break

    while True:
        try:
            print(f"\n--- Welcome {name_input} To Adamstown Library Management System ---")
            print("1. View List of Books")
            print("2. View List of Students")
            print("3. Lend a Book")
            print("4. Return a Book")
            print("5. View Borrowed Books by a Student")
            print("6. Add New Book")
            print("7. Delete a Book")
            print("8. Add New Student")
            print("9. Delete Student")
            print("10. Exit")

            choice = input(f"Enter your choice {name_input}: ")

            # Try to convert the input into an integer
            choice = int(choice)  # This will raise a ValueError if input is not a valid integer

            if choice == 1:
                view_books()
            elif choice == 2:
                view_students()
            elif choice == 3:
                lend_book()
            elif choice == 4:
                return_book()
            elif choice == 5:
                view_books_borrowed_by_student()
            elif choice == 6:
                add_new_book()
            elif choice == 7:
                delete_book()
            elif choice == 8:
                add_new_student()
            elif choice == 9:
                delete_student()
            elif choice == 10:
                while True:  # Loop to repeatedly ask for valid confirmation
                    confirm = input("Are you sure you want to exit? (y/n): ").lower()
                    if confirm == 'y':
                        print(f"Goodbye, {name_input}! You have been signed out!")
                        exit()  # Explicitly terminate the program
                    elif confirm == 'n':
                        print("Returning to the main menu...")
                        break  # Break out of confirmation loop, returning to the main menu
                    else:
                        print("Error: Please enter 'y' for yes or 'n' for no.")  # Invalid input, loop continues
            else:
                print("Please select between 1 - 10")
        except ValueError:# The value error makes sure that the user can only input numbers from 1-10 and if any other, it will trigger an error
            print("Please enter a valid number.")
if __name__ == "__main__":
    main()
