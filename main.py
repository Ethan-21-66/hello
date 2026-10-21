"""A small command-line library management system."""

from dataclasses import dataclass


@dataclass
class Book:
	book_id: int
	title: str
	author: str
	borrowed: bool = False


class Library:
	def __init__(self) -> None:
		self.books: dict[int, Book] = {}
		self.next_id = 1

	def add_book(self, title: str, author: str) -> Book:
		book = Book(self.next_id, title.strip(), author.strip())
		self.books[book.book_id] = book
		self.next_id += 1
		return book

	def search(self, query: str) -> list[Book]:
		query = query.lower().strip()
		return [
			book
			for book in self.books.values()
			if query in book.title.lower() or query in book.author.lower()
		]

	def borrow(self, book_id: int) -> str:
		book = self.books.get(book_id)
		if book is None:
			return "Book not found."
		if book.borrowed:
			return "That book is already borrowed."
		book.borrowed = True
		return f'Borrowed "{book.title}".'

	def return_book(self, book_id: int) -> str:
		book = self.books.get(book_id)
		if book is None:
			return "Book not found."
		if not book.borrowed:
			return "That book is already available."
		book.borrowed = False
		return f'Returned "{book.title}".'

	def display(self, books: list[Book] | None = None) -> None:
		books = list(self.books.values()) if books is None else books
		if not books:
			print("No books found.")
			return
		for book in books:
			status = "Borrowed" if book.borrowed else "Available"
			print(f"{book.book_id}. {book.title} — {book.author} [{status}]")


def read_id() -> int | None:
	try:
		return int(input("Book ID: "))
	except ValueError:
		print("Please enter a valid numeric ID.")
		return None


def main() -> None:
	library = Library()
	for title, author in (
		("The Hobbit", "J. R. R. Tolkien"),
		("1984", "George Orwell"),
	):
		library.add_book(title, author)

	while True:
		print("\nLibrary Management System")
		print("1. List books\n2. Add book\n3. Search\n4. Borrow\n5. Return\n6. Exit")
		choice = input("Choose an option: ").strip()

		if choice == "1":
			library.display()
		elif choice == "2":
			title = input("Title: ").strip()
			author = input("Author: ").strip()
			if title and author:
				book = library.add_book(title, author)
				print(f"Added book #{book.book_id}.")
			else:
				print("Title and author are required.")
		elif choice == "3":
			library.display(library.search(input("Search: ")))
		elif choice in {"4", "5"}:
			book_id = read_id()
			if book_id is not None:
				print(library.borrow(book_id) if choice == "4" else library.return_book(book_id))
		elif choice == "6":
			print("Goodbye!")
			break
		else:
			print("Invalid option.")


if __name__ == "__main__":
	main()
