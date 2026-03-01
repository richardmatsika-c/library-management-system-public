## The Target Architecture
- Single Responsibilty Principle: Model -> View -> Controller Pattern

- `data_structures.py`: This file will solely contain the raw, custom-built algorithms and nodes (`BookNode`, `LinkedList`, `ReservationQueue`, `HistoryStack`).

- `database.py`: This will handle the mock data storage, specifically the `MemberRegistry` which acts as your hash-map database.

- `controller.py`: This will house the `Library` class. It will import your data structures and act as the brain of the operation, connecting books to members and handling the rules of borrowing and returning.

- `gui.py`: This will contain the `LibraryApp` Tkinter class and all the visual styling. It will only handle buttons, inputs, and tables, passing the actual work to the controller.

- `main.py`: A tiny, clean entry point that simply imports the GUI and starts the application loop.