# data_structure.py

from datetime import datetime
from typing import Optional


# -- 1. NODE for Linked List --
class BookNode:
    """A single node in the book linked list."""

    def __init__(self, book_id, title, author, genre, copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.copies = copies  # Total copies
        self.available = copies  # copies currently available
        self.next: Optional["BookNode"] = None  # pointer to next node


# -- 2. LINKED LIST - Book Catalog --
class LinkedList:
    """Singly linked list that stores all books in the library catalog."""

    head: Optional[BookNode]
    tail: Optional[BookNode]

    def __init__(self):
        self.head = None
        self.tail = None  # Always points to last node
        self.count = 0

    # Insert at end — now O(1)
    def insert(self, book_id, title, author, genre, copies):
        new_node = BookNode(book_id, title, author, genre, copies)

        if self.head is None:  # Empty list
            self.head = new_node  # First node is both head AND tail
            self.tail = new_node
        else:
            if self.tail is not None:  # List has nodes
                self.tail.next = new_node  # Old last node points to new node
                self.tail = new_node  # Update tail to new last node

        self.count += 1

    # Delete by book_id
    def delete(self, book_id):
        current = self.head
        previous: Optional[BookNode] = None

        while current:
            if current.book_id == book_id:
                # Case 1: Deleting the ONLY node (head == tail)
                if self.head == self.tail:
                    self.head = None
                    self.tail = None
                # Case 2: Deleting the FIRST node (head)
                elif current == self.head:
                    self.head = current.next
                # Case 3: Deleting the LAST node (tail)
                elif current == self.tail:
                    if previous is not None:
                        previous.next = None  # Disconnect last node
                        self.tail = previous  # Move tail back
                # Case 4: Deleting MIDDLE node
                else:
                    if previous is not None:
                        previous.next = current.next
                self.count -= 1
                return True
            previous = current
            current = current.next

        return False

    # Find book by id
    def find_by_id(self, book_id):
        if self.tail and self.tail.book_id == book_id:
            return self.tail

        current = self.head
        while current:
            if current.book_id == book_id:
                return current
            current = current.next
        return None

    # Return all books as a list (for sorting / display)
    def to_list(self):
        books = []
        current = self.head
        while current:
            books.append(current)
            current = current.next
        return books

    def linear_search(self, query, field="title"):
        """O(n) - Searches node-by-node for a partial string match."""
        results = []
        query = query.lower()
        current = self.head
        while current:
            val = getattr(current, field).lower()
            if query in val:
                results.append(current)
            current = current.next
        return results

    # -- ALGORITHM: In-Place Merge Sort ---
    def merge_sort(self, key="title"):
        """
        O(n log n) - Wrapper method to initiate recursive merge sort.
        Sorts the linked list by manipulating pointers, Not swapping data.
        """
        if self.head is None or self.head.next is None:
            return
        self.head = self._merge_sort_recursive(self.head, key)

    def _get_middle(self, head):
        """O(n) - Uses the slow/fast pointer technique to find the middle node."""
        if not head:
            return head
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def _merge(self, left, right, key):
        """O(n) - Merges two sorted linked lists back together."""
        if not left:
            return right
        if not right:
            return left

        val_left = getattr(left, key).lower()
        val_right = getattr(right, key).lower()

        # Compare and recursively link the smaller node
        if val_left <= val_right:
            result = left
            result.next = self._merge(left.next, right, key)
        else:
            result = right
            result.next = self._merge(left, right.next, key)
        return result

    def _merge_sort_recursive(self, head, key):
        """Recursive core of the merge sort algorithm."""
        if not head or not head.next:
            return head

        # 1. Split the list into two halves
        middle = self._get_middle(head)
        next_to_middle = middle.next
        middle.next = None  # Sever the link

        # 2. Recursively sort both halves
        left = self._merge_sort_recursive(head, key)
        right = self._merge_sort_recursive(next_to_middle, key)

        # 3. Merge the sorted halves
        return self._merge(left, right, key)


# 2. QUEUE - Manual Node-Based Reservation Wait list
class QueNode:
    """
    A single node in the reservation queue.
    Each node stores one reservation request + a pointer to the next node.
    """

    def __init__(self, member_id, member_name, book_id, book_title):
        # Reservation details kept separately for easy access
        self.member_id = member_id
        self.member_name = member_name
        self.book_id = book_id
        self.book_title = book_title

        # Explicit 'next' pointer so Pylance knows it exists
        self.next: Optional["QueNode"] = None

        # Package the reservation data for simple return during dequeue
        self.data = {
            "member_id": member_id,
            "member_name": member_name,
            "book_id": book_id,
            "book_title": book_title,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }


class ReservationQueue:
    """
    A FIFO queue used for handling book reservations.

    Implemented as a manually linked structure (like a linked list),
    supporting O(1) enqueue and dequeue operations.
    """

    def __init__(self):
        # Front: node where dequeuing happens
        # Rear: node where enqueuing happens
        self.front: Optional[QueNode] = None
        self.rear: Optional[QueNode] = None
        self._count = 0

    def enqueue(self, member_id, member_name, book_id, book_title):
        """
        Add a new reservation to the *rear* of the queue.
        Runs in O(1) time because we maintain a rear pointer.
        """
        new_node = QueNode(member_id, member_name, book_id, book_title)

        if self.rear is None:
            # Queue is empty → front and rear both become the new node
            self.front = self.rear = new_node
        else:
            # Pylance: rear is Optional, so assert to guarantee safety
            assert self.rear is not None
            self.rear.next = new_node  # Link old last node to new node
            self.rear = new_node  # Move rear pointer

        self._count += 1

    def dequeue(self):
        """
        Remove and return the reservation at the *front* of the queue.
        Runs in O(1) time.
        """
        if self.front is None:  # Queue empty
            return None
        temp = self.front  # Node being removed
        self.front = temp.next  # Move front pointer forward
        # If queue is now empty, reset rear pointer as well
        if self.front is None:
            self.rear = None

        self._count -= 1
        # Return the packaged reservation data
        return temp.data

    def peek(self):
        """O(1) - Look at the front item without removing it."""
        return self.front.data if self.front else None

    def is_empty(self):
        """O(1) - Check if queue has nodes."""
        return self.front is None

    def size(self):
        """O(1) - Return tracked count."""
        return self._count

    def to_list(self):
        """O(n) - Helper to yield data for GUI display."""
        items = []
        current = self.front
        while current:
            items.append(current.data)
            current = current.next
        return items

    def remove_member(self, member_id, book_id):
        """
        O(n) - Special case: Wait list cancellation.
        Requires traversing to find and delete a specific node.
        """
        current = self.front
        prev = None

        while current:
            if (
                current.data["member_id"] == member_id
                and current.data["book_id"] == book_id
            ):
                # Rewire pointers to drop the target node
                if prev:
                    prev.next = current.next
                else:
                    self.front = current.next

                # If we deleted the rear node, update the rear pointer
                if current == self.rear:
                    self.rear = prev

                self._count -= 1
                return True

            prev = current
            current = current.next
        return False


# 3. STACK - Borrow / Return History
class HistoryStack:
    """
    LIFO Stack that records every borrow and return action.
    """

    def __init__(self):
        self._stack = []

    def push(self, action, member_id, member_name, book_id, book_title):
        """O(1) - Push to top of stack."""
        entry = {
            "action": action,
            "member_id": member_id,
            "member_name": member_name,
            "book_id": book_id,
            "book_title": book_title,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self._stack.append(entry)

    def pop(self):
        """O(1) - Remove and return top of stack."""
        return self._stack.pop() if self._stack else None

    def peek(self):
        """O(1) - Look at top of stack without removing."""
        return self._stack[-1] if self._stack else None

    def is_empty(self):
        """O(1)"""
        return len(self._stack) == 0

    def to_list(self):
        """O(n) - Return reserved for GUI (newest first)."""
        return list(reversed(self._stack))
