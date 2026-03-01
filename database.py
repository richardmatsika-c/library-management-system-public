# database.py

# Data Persistence Layer

from datetime import datetime


class MemberRegistry:
    """
    Hash-map for O(1) average member lookup.
    Each member tracks which books they currently have borrowed.
    """

    def __init__(self):
        self._members = {}  # {member_id: member_dict}

    def add(self, member_id, name, email, phone):
        if member_id in self._members:
            return False, "Member ID already exists."
        self._members[member_id] = {
            "member_id": member_id,
            "name": name,
            "email": email,
            "phone": phone,
            "borrowed": [],
            "joined": datetime.now().strftime("%Y-%m-%d"),
        }
        return True, "Member registered successfully."

    def remove(self, member_id):
        if member_id not in self._members:
            return False, "Member not found."
        if self._members[member_id]["borrowed"]:
            return False, "Member still has borrowed books."
        del self._members[member_id]
        return True, "Member removed."

    def find(self, member_id):
        return self._members.get(member_id)

    def all(self):
        return list(self._members.values())

    def borrow_book(self, member_id, book_id):
        m = self._members.get(member_id)
        if m:
            m["borrowed"].remove(book_id)
