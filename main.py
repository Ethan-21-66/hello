"""A small, in-memory library management system."""

from dataclasses import dataclass


@dataclass
class Book:
	book_id: int
	title: str
	author: str
	available: bool = True
	borrowed_by: str | None = None


class Library:
	def __init__(self) -> None:
		self.books: dict[int, Book] = {}

	def add_book(self, title: str, author: str) -> Book:
		book_id = max(self.books, default=0) + 1
		book = Book(book_id, title.strip(), author.strip())
		self.books[book_id] = book
		return book

	def list_books(self) -> list[Book]:
		return list(self.books.values())

	def search(self, query: str) -> list[Book]:
		query = query.lower()
		return [
			book
			for book in self.books.values()
			if query in book.title.lower() or query in book.author.lower()
		]

	def borrow_book(self, book_id: int, member: str) -> str:
		book = self.books.get(book_id)
		if book is None:
			return "Book not found."
		if not book.available:
			return f"Book is already borrowed by {book.borrowed_by}."
		book.available = False
		book.borrowed_by = member.strip()
		return "Book borrowed successfully."

	def return_book(self, book_id: int) -> str:
		book = self.books.get(book_id)
		if book is None:
			return "Book not found."
		if book.available:
			return "Book is already available."
		book.available = True
		book.borrowed_by = None
		return "Book returned successfully."


def display_books(books: list[Book]) -> None:
	if not books:
		print("No books found.")
		return
	for book in books:
		status = "Available" if book.available else f"Borrowed by {book.borrowed_by}"
		print(f"{book.book_id}. {book.title} by {book.author} — {status}")


def main() -> None:
	library = Library()
	library.add_book("The Alchemist", "Paulo Coelho")
	library.add_book("1984", "George Orwell")

	actions = {
		"1": lambda: display_books(library.list_books()),
		"2": lambda: library.add_book(input("Title: "), input("Author: ")),
		"3": lambda: display_books(library.search(input("Search: "))),
		"4": lambda: print(library.borrow_book(int(input("Book ID: ")), input("Member: "))),
		"5": lambda: print(library.return_book(int(input("Book ID: ")))),
	}

	while True:
		print("\nLibrary Management System")
		print("1. List books\n2. Add book\n3. Search books\n4. Borrow book\n5. Return book\n6. Exit")
		choice = input("Choose an option: ").strip()
		if choice == "6":
			print("Goodbye!")
			break
		action = actions.get(choice)
		if action is None:
			print("Invalid option.")
			continue
		try:
			action()
		except ValueError:
			print("Please enter a valid book ID.")


if __name__ == "__main__":
	main()
