# 📚 CUITM205: Library Management System

A high-performance, modern GUI application for managing library operations. This project was engineered from scratch to demonstrate the practical application of fundamental data structures and algorithms, utilizing a clean Model-View-Controller (MVC) architecture.

## 🚀 Features
* **Modern Interface:** Built with `customtkinter` for a sleek, responsive user experience.
* **Smart Cataloging:** Add, remove, sort, and search library inventory.
* **Automated Waitlists:** FIFO queue system automatically assigns newly returned books to the next member in line.
* **Action History:** Chronological feed of library activity with full Undo (LIFO) capabilities.
* **Member Management:** Track registered users and their current borrowed items.

## 🧠 Data Structures & Algorithms
This system avoids relying entirely on standard Python lists, implementing manual, pointer-based structures to handle core logic:

* **Singly Linked List:** Manages the entire book catalog dynamically in memory.
* **Manual Queue (FIFO):** A node-based queue guaranteeing O(1) enqueue/dequeue operations for book reservations.
* **Stack (LIFO):** Tracks borrow/return history, allowing instant O(1) "Undo" functionality.
* **Hash Map (Dictionary):** Provides O(1) average lookup times for member records.
* **In-Place Merge Sort:** An O(n log n) divide-and-conquer algorithm that sorts the linked list by directly manipulating node pointers.
* **Linear Search:** An O(n) traversal algorithm for partial string matching across titles, authors, and genres.

## 🏗️ Architecture (MVC)
The codebase is heavily modularized into distinct layers:
1. `data_structures.py`: Raw mathematical logic and custom nodes.
2. `database.py`: State persistence and data mapping.
3. `controller.py`: The business logic bridging data and the view.
4. `mmorden_gui.py`: The visual interface and frame routing.
5. `main.py`: The lightweight application entry point.

## 💻 How to Run

**Option A: Run the Executable (Recommended)**
Navigate to the `dist/` folder and double-click `main.exe`. No installation or Python environment required.

**Option B: Run from Source**
1. Ensure Python 3.10+ is installed.
2. Clone this repository and navigate to the root folder.
3. Install the required UI library:
   ```bash
   pip install -r requirements.txt