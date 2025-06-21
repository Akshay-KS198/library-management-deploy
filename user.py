from library import Library

class User(Library):
    def __init__(self, book):
        self.book = book
        super().__init__(book, None)

    def borrow_book(self):
        if self.book in self._books and self._books[self.book] > 0:
            print(f"---------Your Book--------\n **********{self.book}********** \n is issued")
            old_count = self._books[self.book]
            self._books[self.book] = old_count - 1
        else:
            print(f"Your Book '{self.book}' is Not Available")

    def return_book(self):
        if self.book in self._books:
            old_count = self._books[self.book]
            self._books[self.book] = old_count + 1
            print(f"---------Your Book--------\n **********{self.book}********** \n is received")

while(True):
    print("Welcome to Library, Enter who are you")
    print("Press 1 for Library Admin: ")
    print("Press 2 for User: ")
    print("Press 3 to exit: ")

    choice = int(input("Enter your choice: "))

    if (choice == 1):
        print("-------You are Admin-------\n Enter your choice")
        print("Press 1 to add new book")
        print("Press 2 to remove a existing book")
        print("Press 3 to exit: ")

        sub_choice = int(input("Enter your choice: "))
        if (sub_choice == 1):
            book = input("Enter the name of the book that you are going to add: ")
            availability = int(input("Enter the availability: "))

            book_entry = Library(book,availability)
            book_entry.add_books()
            book_entry.display_books_details()

        elif (sub_choice == 2):
            book = input("Enter the name of the book that you are going to remove: ")
            book_entry = Library(book)
            book_entry.remove_book()
            book_entry.display_books_details()

        elif (sub_choice == 3):
            break

    elif (choice == 2):
        print("-------You are User-------\n")
        book = input("You are user, Enter the name of the book that you want: ")
        user = User(book)
        user.borrow_book()
        user.display_books_details()

    elif (choice == 3):
        break
