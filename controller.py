# controller.py

# Business Logic

from data_structures import LinkedList, ReservationQueue, HistoryStack
from database import MemberRegistry


class Library:
    def __init__(self):
        self.catalog = LinkedList()
        self.members = MemberRegistry()
        self.reservations = ReservationQueue()
        self.history = HistoryStack()
        self._next_book_id = 1001
        self._next_member_id = 2001
        self._seed_data()

    # -- Seed demo data --
    def _seed_data(self):
        books = [
            ("Introduction to Algorithms", "Cormen et al.", "Computer Science", 3),
            ("Clean Code", "Robert C. Martin", "Software Engineering", 2),
            ("The Pragmatic Programmer", "Hunt & Thomas", "Software Engineering", 2),
            ("Data Structures in Python", "Goodrich et al.", "Computer Science", 4),
            ("Design Patterns", "Gang of Four", "Software Engineering", 2),
            (
                "Artificial Intelligence: A Guide",
                "Stuart Russell",
                "Computer Science",
                1,
            ),
            ("Database System Concepts", "Silberschatz et al.", "Databases", 3),
            ("Operating System Concepts", "Silberschatz et al.", "Systems", 2),
            ("Computer Networks", "Tanenbaum", "Networking", 3),
            ("Discrete Mathematics", "Kenneth Rosen", "Mathematics", 2),
        ]
        for title, author, genre, copies in books:
            self.catalog.insert(self._next_book_id, title, author, genre, copies)
            self._next_book_id += 1

        members = [
            ("Alice Moyo", "alice@cut.ac.zw", "0771000001"),
            ("Brian Choto", "brian@cut.ac.zw", "0772000002"),
            ("Carol Dube", "carol@cut.ac.zw", "0773000003"),
        ]
        for name, email, phone in members:
            self.members.add(self._next_member_id, name, email, phone)
            self._next_member_id += 1

    # -- Book operations --
    def add_book(self, title, author, genre, copies):
        if not title or not author:
            return False, "Title and author are required."
        try:
            copies = int(copies)
            if copies < 1:
                raise ValueError
        except ValueError:
            return False, "Copies must be a positive integer."
        self.catalog.insert(self._next_book_id, title, author, genre, copies)
        self._next_book_id += 1
        return True, f"Book '{title}' added (ID {self._next_book_id - 1})."

    def remove_book(self, book_id):
        try:
            book_id = int(book_id)
        except ValueError:
            return False, "Invalid book ID."
        book = self.catalog.find_by_id(book_id)
        if not book:
            return False, "Book not found."
        if book.available < book.copies:
            return False, "Cannot remove: some copies are currently borrowed."
        self.catalog.delete(book_id)
        return True, f"Book, '{book.title}' removed."

    # -- Member Operations --
    def add_member(self, name, email, phone):
        if not name:
            return False, "Name is required."
        ok, msg = self.members.add(self._next_member_id, name, email, phone)
        if ok:
            self._next_member_id += 1
        return ok, msg

    def remove_member(self, member_id):
        try:
            member_id = int(member_id)
        except ValueError:
            return False, "invalid member ID."
        return self.members.remove(member_id)

    # -- Borrow / Return --
    def borrow_book(self, member_id, book_id):
        try:
            member_id = int(member_id)
            book_id = int(book_id)
        except ValueError:
            return False, "Invalid ID(s)."

        member = self.members.find(member_id)
        if not member:
            return False, "Member not found."

        book = self.catalog.find_by_id(book_id)
        if not book:
            return False, "Book not found."

        if book_id in member["borrowed"]:
            return False, "Member already has this book."

        if book.available < 1:
            self.reservations.enqueue(member_id, member["name"], book_id, book.title)
            return False, (
                f"No copies available. {member['name']} has been added."
                f"to the reservation queue for '{book.title}'."
            )

        book.available -= 1
        self.members.borrow_book(self, member_id, book_id)
        try:
            member_id = int(member_id)
            book_id = int(book_id)
        except ValueError:
            return False, "Invalid ID(s)."

        member = self.members.find(member_id)
        if not member:
            return False, "Member not found."

        book = self.catalog.find_by_id(book_id)
        if not book:
            return False, "Book not found."

        if book_id not in member["borrowed"]:
            return False, "This member did not borrow this book."

        book.available += 1
        self.members.return_book(member_id, book_id)
        self.history.push("RETURN", member_id, member["name"], book_id, book.title)

        next_up = None
        for entry in self.reservations.to_list():
            if entry["book_id"] == book_id:
                next_up = entry
                self.reservations.remove_member(entry["member_id"], book_id)
                break

        msg = f"'{book.title}' returned by {member['name']}."
        if next_up:
            msg += f"\n\nNotification: '{next_up['member_name']}' is next in queue - please issue the book."
        return True, msg

    def sort_catalog(self, key="title"):
        self.catalog.merge_sort(key)

    def search(self, query, field="title"):
        return self.catalog.linear_search(query, field)
