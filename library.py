
class Library:
    def __init__(self, book, availability=1):
        self._books = {
            "The Alchemist": 4,
            "To Kill a Mockingbird": 2,
            "1984": 4,
            "Pride and Prejudice": 3,
            "The Great Gatsby": 1,
            "Harry Potter and the Sorcerer's Stone": 5,
            "The Catcher in the Rye": 2,
            "The Hobbit": 7,
            "The Lord of the Rings": 3,
            "Moby Mick": 1
        }
        self.book = book
        self.availability = availability

    def increase_book_count(self):
        old_value = self._books[self.book]
        self._books[self.book] = old_value + self.availability
        print(f"Availability of your book {self.book} has increased from {old_value} to {self._books[self.book]}")
        self.display_books_details()

    def add_books(self):
        if self.book not in self._books:
            self._books[self.book] = self.availability
            print(f"{self.book} is added successfully")
        else:
            print(f"{self.book} already exists")
            addition_choice = input(f"Do you want to increase the existing {self.book} count? ")
            if addition_choice.lower() == "yes":
                self.increase_book_count()

    def remove_book(self):
        if self.book in self._books:
            del self._books[self.book]
            print(f"{self.book} is removed successfully")
        else:
            print(f"{self.book} not found")

    def display_books_details(self):
        for book, availability in self._books.items():
            print(f"Book:- {book}, availability:- {availability}")

    
