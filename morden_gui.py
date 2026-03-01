# gui.py
# ─────────────────────────────────────────────────────────────────────────────
# User Interface Layer (View) - Modern CustomTkinter Edition
# ─────────────────────────────────────────────────────────────────────────────

import customtkinter as ctk
from tkinter import ttk, messagebox
from controller import Library

# ── Color Palette ─────────────────────────────────────────────────────────────
SIDEBAR_BG = "#1e3a8a"  # Deep blue
MAIN_BG = "#f4f6f9"  # Off-white/light gray
CARD_BG = "#ffffff"  # Pure white
TEXT_DARK = "#1f2937"
TEXT_LIGHT = "#ffffff"

C_BLUE = "#3b82f6"
C_GREEN = "#10b981"
C_YELLOW = "#f59e0b"
C_PURPLE = "#8b5cf6"
C_DANGER = "#ef4444"


class ModernLibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Initialize Controller
        self.library = Library()

        # 2. Window Setup
        self.title("Library Management System")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        ctk.set_appearance_mode("light")
        self.configure(fg_color=MAIN_BG)

        # 3. Setup Modern Treeview Styling
        self._setup_treeview_style()

        # 4. Build Layout
        self.frames = {}  # Dictionary to hold our different screens
        self._build_sidebar()

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(
            side="right", fill="both", expand=True, padx=30, pady=30
        )

        # Build all screens
        self._build_dashboard()
        self._build_books()
        self._build_members()
        self._build_borrow()
        self._build_search()
        self._build_history()

        # Start on the Dashboard
        self._select_frame("Dashboard")

    def _setup_treeview_style(self):
        """Forces standard ttk.Treeview to look like a modern web table."""
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=CARD_BG,
            foreground=TEXT_DARK,
            rowheight=35,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=MAIN_BG,
            foreground=TEXT_DARK,
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
        )
        style.map(
            "Treeview",
            background=[("selected", C_BLUE)],
            foreground=[("selected", TEXT_LIGHT)],
        )
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

    def _create_scrollable_tree(self, parent, columns, widths):
        """Helper to create a Treeview with a scrollbar seamlessly attached."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col, w in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="w")

        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)

        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        return frame, tree

    # ── ROUTER LOGIC ──────────────────────────────────────────────────────────
    def _select_frame(self, name):
        """Hides all frames and shows the requested one."""
        for frame in self.frames.values():
            frame.pack_forget()

        self.frames[name].pack(fill="both", expand=True)

        # Refresh data when opening a tab
        if name == "Dashboard":
            self._refresh_dashboard()
        elif name == "Books":
            self._refresh_books()
        elif name == "Members":
            self._refresh_members()
        elif name == "Borrow / Return":
            self._refresh_queue()
        elif name == "History":
            self._refresh_history()

    # ── SIDEBAR ───────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=250, corner_radius=0, fg_color=SIDEBAR_BG
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="📚 LIBRARY MS",
            font=("Segoe UI", 22, "bold"),
            text_color=TEXT_LIGHT,
        ).pack(pady=(30, 40), padx=20, anchor="w")

        nav_items = [
            "Dashboard",
            "Books",
            "Members",
            "Borrow / Return",
            "Search",
            "History",
        ]

        for item in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {item}",
                anchor="w",
                font=("Segoe UI", 14, "bold"),
                fg_color="transparent",
                text_color=TEXT_LIGHT,
                hover_color="#3b82f6",
                corner_radius=15,
                height=45,
                command=lambda n=item: self._select_frame(n),
            )
            btn.pack(fill="x", padx=15, pady=5)

    # ── DASHBOARD SCREEN ──────────────────────────────────────────────────────
    def _build_dashboard(self):
        dash_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["Dashboard"] = dash_frame

        ctk.CTkLabel(
            dash_frame,
            text="Hello, Librarian! 👋",
            font=("Segoe UI", 28, "bold"),
            text_color=TEXT_DARK,
        ).pack(anchor="w", pady=(0, 20))

        # Stats Row
        self.stats_frame = ctk.CTkFrame(dash_frame, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=(0, 30))
        self.stats_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")

        self.stat_labels = {}
        stat_configs = [
            ("Total Books", C_BLUE),
            ("Registered Members", C_GREEN),
            ("Books Borrowed", C_YELLOW),
            ("Queue Reservations", C_PURPLE),
        ]

        for i, (title, color) in enumerate(stat_configs):
            card = ctk.CTkFrame(
                self.stats_frame, fg_color=color, corner_radius=15, height=120
            )
            card.grid(row=0, column=i, padx=10, sticky="nsew")
            card.pack_propagate(False)

            val_lbl = ctk.CTkLabel(
                card, text="0", font=("Segoe UI", 36, "bold"), text_color=TEXT_LIGHT
            )
            val_lbl.pack(pady=(25, 0))
            self.stat_labels[title] = val_lbl
            ctk.CTkLabel(
                card, text=title, font=("Segoe UI", 14), text_color=TEXT_LIGHT
            ).pack()

        # Recent Activity Feed
        feed_card = ctk.CTkFrame(dash_frame, fg_color=CARD_BG, corner_radius=15)
        feed_card.pack(fill="both", expand=True, padx=10)

        ctk.CTkLabel(
            feed_card,
            text="Recent Transactions",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=20, pady=20)

        tree_container, self.feed_tree = self._create_scrollable_tree(
            feed_card, ("Time", "Action", "Member", "Book"), [160, 100, 180, 340]
        )
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _refresh_dashboard(self):
        borrowed_count = sum(len(m["borrowed"]) for m in self.library.members.all())

        self.stat_labels["Total Books"].configure(text=str(self.library.catalog.count))
        self.stat_labels["Registered Members"].configure(
            text=str(len(self.library.members.all()))
        )
        self.stat_labels["Books Borrowed"].configure(text=str(borrowed_count))
        self.stat_labels["Queue Reservations"].configure(
            text=str(self.library.reservations.size())
        )

        self.feed_tree.delete(*self.feed_tree.get_children())
        for entry in self.library.history.to_list()[:15]:  # Show last 15 actions
            self.feed_tree.insert(
                "",
                "end",
                values=(
                    entry["timestamp"],
                    entry["action"],
                    f"{entry['member_name']} ({entry['member_id']})",
                    entry["book_title"],
                ),
            )

    # ── BOOKS SCREEN ──────────────────────────────────────────────────────────
    def _build_books(self):
        books_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["Books"] = books_frame
        books_frame.columnconfigure(0, weight=1)
        books_frame.columnconfigure(1, weight=3)
        books_frame.rowconfigure(0, weight=1)

        # Left Column: Manage Books
        controls_card = ctk.CTkFrame(books_frame, fg_color=CARD_BG, corner_radius=15)
        controls_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(
            controls_card,
            text="Add New Book",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=20, pady=(20, 10))
        self.bk_title = ctk.CTkEntry(
            controls_card, placeholder_text="Book Title *", height=40
        )
        self.bk_title.pack(fill="x", padx=20, pady=5)
        self.bk_author = ctk.CTkEntry(
            controls_card, placeholder_text="Author *", height=40
        )
        self.bk_author.pack(fill="x", padx=20, pady=5)
        self.bk_genre = ctk.CTkEntry(controls_card, placeholder_text="Genre", height=40)
        self.bk_genre.pack(fill="x", padx=20, pady=5)
        self.bk_copies = ctk.CTkEntry(
            controls_card, placeholder_text="Total Copies *", height=40
        )
        self.bk_copies.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(
            controls_card,
            text="Add Book",
            fg_color=C_BLUE,
            hover_color="#2563eb",
            height=40,
            command=self._add_book,
        ).pack(fill="x", padx=20, pady=15)

        ctk.CTkFrame(controls_card, height=1, fg_color=MAIN_BG).pack(
            fill="x", padx=20, pady=10
        )

        ctk.CTkLabel(
            controls_card,
            text="Remove Book",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=20, pady=(10, 10))
        self.bk_del_id = ctk.CTkEntry(
            controls_card, placeholder_text="Book ID", height=40
        )
        self.bk_del_id.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(
            controls_card,
            text="Remove Book",
            fg_color=C_DANGER,
            hover_color="#b91c1c",
            height=40,
            command=self._remove_book,
        ).pack(fill="x", padx=20, pady=15)

        ctk.CTkFrame(controls_card, height=1, fg_color=MAIN_BG).pack(
            fill="x", padx=20, pady=10
        )

        ctk.CTkLabel(
            controls_card,
            text="Sort Catalog",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=20, pady=(10, 10))
        self.sort_key = ctk.CTkOptionMenu(
            controls_card, values=["title", "author", "genre"], height=40
        )
        self.sort_key.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(
            controls_card,
            text="Sort (Merge Sort)",
            fg_color=C_YELLOW,
            hover_color="#d97706",
            text_color=TEXT_DARK,
            height=40,
            command=self._sort_books,
        ).pack(fill="x", padx=20, pady=15)

        # Right Column: Catalog Treeview
        table_card = ctk.CTkFrame(books_frame, fg_color=CARD_BG, corner_radius=15)
        table_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(
            table_card,
            text="Book Catalog",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=20, pady=20)
        tree_container, self.books_tree = self._create_scrollable_tree(
            table_card,
            ("ID", "Title", "Author", "Genre", "Copies", "Available"),
            [60, 250, 150, 120, 70, 80],
        )
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _refresh_books(self):
        self.books_tree.delete(*self.books_tree.get_children())
        for b in self.library.catalog.to_list():
            self.books_tree.insert(
                "",
                "end",
                values=(b.book_id, b.title, b.author, b.genre, b.copies, b.available),
            )

    def _add_book(self):
        ok, msg = self.library.add_book(
            self.bk_title.get().strip(),
            self.bk_author.get().strip(),
            self.bk_genre.get().strip(),
            self.bk_copies.get().strip(),
        )
        if ok:
            for v in [self.bk_title, self.bk_author, self.bk_genre, self.bk_copies]:
                v.delete(0, "end")
            self._refresh_books()
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    def _remove_book(self):
        ok, msg = self.library.remove_book(self.bk_del_id.get().strip())
        if ok:
            self.bk_del_id.delete(0, "end")
            self._refresh_books()
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    def _sort_books(self):
        self.library.sort_catalog(self.sort_key.get())
        self._refresh_books()
        messagebox.showinfo(
            "Sorted", f"Catalog sorted by {self.sort_key.get()} using Merge Sort."
        )

    # ── MEMBERS SCREEN ────────────────────────────────────────────────────────
    def _build_members(self):
        members_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["Members"] = members_frame
        members_frame.columnconfigure(0, weight=1)
        members_frame.columnconfigure(1, weight=3)
        members_frame.rowconfigure(0, weight=1)

        # Left Column: Manage Members
        controls_card = ctk.CTkFrame(members_frame, fg_color=CARD_BG, corner_radius=15)
        controls_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(
            controls_card,
            text="Register Member",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=20, pady=(20, 10))
        self.mb_name = ctk.CTkEntry(
            controls_card, placeholder_text="Full Name *", height=40
        )
        self.mb_name.pack(fill="x", padx=20, pady=5)
        self.mb_email = ctk.CTkEntry(controls_card, placeholder_text="Email", height=40)
        self.mb_email.pack(fill="x", padx=20, pady=5)
        self.mb_phone = ctk.CTkEntry(controls_card, placeholder_text="Phone", height=40)
        self.mb_phone.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(
            controls_card,
            text="Register",
            fg_color=C_GREEN,
            hover_color="#059669",
            height=40,
            command=self._add_member,
        ).pack(fill="x", padx=20, pady=15)

        ctk.CTkFrame(controls_card, height=1, fg_color=MAIN_BG).pack(
            fill="x", padx=20, pady=10
        )

        ctk.CTkLabel(
            controls_card,
            text="Remove Member",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=20, pady=(10, 10))
        self.mb_del_id = ctk.CTkEntry(
            controls_card, placeholder_text="Member ID", height=40
        )
        self.mb_del_id.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(
            controls_card,
            text="Remove",
            fg_color=C_DANGER,
            hover_color="#b91c1c",
            height=40,
            command=self._remove_member,
        ).pack(fill="x", padx=20, pady=15)

        # Right Column: Members Directory
        table_card = ctk.CTkFrame(members_frame, fg_color=CARD_BG, corner_radius=15)
        table_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(
            table_card,
            text="Member Directory",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=20, pady=20)
        tree_container, self.members_tree = self._create_scrollable_tree(
            table_card,
            ("ID", "Name", "Email", "Phone", "Borrowed", "Joined"),
            [80, 200, 200, 130, 90, 100],
        )
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _refresh_members(self):
        self.members_tree.delete(*self.members_tree.get_children())
        for m in self.library.members.all():
            self.members_tree.insert(
                "",
                "end",
                values=(
                    m["member_id"],
                    m["name"],
                    m["email"],
                    m["phone"],
                    len(m["borrowed"]),
                    m["joined"],
                ),
            )

    def _add_member(self):
        ok, msg = self.library.add_member(
            self.mb_name.get().strip(),
            self.mb_email.get().strip(),
            self.mb_phone.get().strip(),
        )
        if ok:
            for v in [self.mb_name, self.mb_email, self.mb_phone]:
                v.delete(0, "end")
            self._refresh_members()
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    def _remove_member(self):
        ok, msg = self.library.remove_member(self.mb_del_id.get().strip())
        if ok:
            self.mb_del_id.delete(0, "end")
            self._refresh_members()
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    # ── BORROW / RETURN SCREEN ────────────────────────────────────────────────
    def _build_borrow(self):
        br_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["Borrow / Return"] = br_frame
        br_frame.columnconfigure((0, 1), weight=1)
        br_frame.rowconfigure(1, weight=1)

        # Borrow Card
        borrow_card = ctk.CTkFrame(br_frame, fg_color=CARD_BG, corner_radius=15)
        borrow_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 20))
        ctk.CTkLabel(
            borrow_card,
            text="Borrow a Book",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=20, pady=20)

        input_frame = ctk.CTkFrame(borrow_card, fg_color="transparent")
        input_frame.pack(fill="x", padx=20)
        self.br_member = ctk.CTkEntry(
            input_frame, placeholder_text="Member ID", width=140, height=40
        )
        self.br_member.pack(side="left", padx=(0, 10), expand=True, fill="x")
        self.br_book = ctk.CTkEntry(
            input_frame, placeholder_text="Book ID", width=140, height=40
        )
        self.br_book.pack(side="left", padx=(0, 10), expand=True, fill="x")
        ctk.CTkButton(
            input_frame,
            text="Borrow",
            fg_color=C_BLUE,
            width=100,
            height=40,
            command=self._borrow,
        ).pack(side="right")

        # Return Card
        return_card = ctk.CTkFrame(br_frame, fg_color=CARD_BG, corner_radius=15)
        return_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 20))
        ctk.CTkLabel(
            return_card,
            text="Return a Book",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=20, pady=20)

        ret_input_frame = ctk.CTkFrame(return_card, fg_color="transparent")
        ret_input_frame.pack(fill="x", padx=20)
        self.rt_member = ctk.CTkEntry(
            ret_input_frame, placeholder_text="Member ID", width=140, height=40
        )
        self.rt_member.pack(side="left", padx=(0, 10), expand=True, fill="x")
        self.rt_book = ctk.CTkEntry(
            ret_input_frame, placeholder_text="Book ID", width=140, height=40
        )
        self.rt_book.pack(side="left", padx=(0, 10), expand=True, fill="x")
        ctk.CTkButton(
            ret_input_frame,
            text="Return",
            fg_color=C_GREEN,
            hover_color="#059669",
            width=100,
            height=40,
            command=self._return,
        ).pack(side="right")

        # Queue Card
        queue_card = ctk.CTkFrame(br_frame, fg_color=CARD_BG, corner_radius=15)
        queue_card.grid(row=1, column=0, columnspan=2, sticky="nsew")
        ctk.CTkLabel(
            queue_card,
            text="Reservation Queue (FIFO)",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=20, pady=20)

        tree_container, self.queue_tree = self._create_scrollable_tree(
            queue_card,
            ("#", "Member ID", "Member Name", "Book ID", "Book Title", "Queued At"),
            [40, 90, 180, 80, 300, 140],
        )
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _refresh_queue(self):
        self.queue_tree.delete(*self.queue_tree.get_children())
        for i, e in enumerate(self.library.reservations.to_list(), 1):
            self.queue_tree.insert(
                "",
                "end",
                values=(
                    i,
                    e["member_id"],
                    e["member_name"],
                    e["book_id"],
                    e["book_title"],
                    e["timestamp"],
                ),
            )

    def _borrow(self):
        ok, msg = self.library.borrow_book(
            self.br_member.get().strip(), self.br_book.get().strip()
        )
        if ok:
            self.br_member.delete(0, "end")
            self.br_book.delete(0, "end")
            self._refresh_queue()
            messagebox.showinfo("Success", msg)
        else:
            self._refresh_queue()  # In case they were added to the waitlist
            messagebox.showwarning("Notice", msg)

    def _return(self):
        ok, msg = self.library.return_book(
            self.rt_member.get().strip(), self.rt_book.get().strip()
        )
        if ok:
            self.rt_member.delete(0, "end")
            self.rt_book.delete(0, "end")
            self._refresh_queue()
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    # ── SEARCH SCREEN ─────────────────────────────────────────────────────────
    def _build_search(self):
        search_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["Search"] = search_frame
        search_frame.columnconfigure(0, weight=1)
        search_frame.rowconfigure(1, weight=1)

        # Search Bar Card
        bar_card = ctk.CTkFrame(search_frame, fg_color=CARD_BG, corner_radius=15)
        bar_card.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        controls_frame = ctk.CTkFrame(bar_card, fg_color="transparent")
        controls_frame.pack(fill="x", padx=20, pady=20)

        self.search_var = ctk.StringVar()
        se = ctk.CTkEntry(
            controls_frame,
            textvariable=self.search_var,
            placeholder_text="Enter search query...",
            height=40,
            width=400,
        )
        se.pack(side="left", padx=(0, 15))
        se.bind("<Return>", lambda e: self._do_search())

        self.search_field = ctk.CTkOptionMenu(
            controls_frame, values=["title", "author", "genre"], height=40
        )
        self.search_field.pack(side="left", padx=(0, 15))

        ctk.CTkButton(
            controls_frame,
            text="Search",
            fg_color=C_BLUE,
            height=40,
            command=self._do_search,
        ).pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            controls_frame,
            text="Show All",
            fg_color=C_YELLOW,
            text_color=TEXT_DARK,
            hover_color="#d97706",
            height=40,
            command=self._show_all,
        ).pack(side="left")

        # Results Card
        res_card = ctk.CTkFrame(search_frame, fg_color=CARD_BG, corner_radius=15)
        res_card.grid(row=1, column=0, sticky="nsew")

        ctk.CTkLabel(
            res_card,
            text="Search Results",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=20, pady=20)

        tree_container, self.search_tree = self._create_scrollable_tree(
            res_card,
            ("ID", "Title", "Author", "Genre", "Copies", "Available"),
            [60, 300, 180, 130, 70, 80],
        )
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self._show_all()

    def _do_search(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Input required", "Please enter a search term.")
            return
        results = self.library.search(query, self.search_field.get())
        self.search_tree.delete(*self.search_tree.get_children())
        for b in results:
            self.search_tree.insert(
                "",
                "end",
                values=(b.book_id, b.title, b.author, b.genre, b.copies, b.available),
            )
        if not results:
            messagebox.showinfo("No results", f"No books found matching '{query}'.")

    def _show_all(self):
        self.search_tree.delete(*self.search_tree.get_children())
        for b in self.library.catalog.to_list():
            self.search_tree.insert(
                "",
                "end",
                values=(b.book_id, b.title, b.author, b.genre, b.copies, b.available),
            )

    # ── HISTORY SCREEN ────────────────────────────────────────────────────────
    def _build_history(self):
        hist_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["History"] = hist_frame
        hist_frame.columnconfigure(0, weight=1)
        hist_frame.rowconfigure(0, weight=1)

        card = ctk.CTkFrame(hist_frame, fg_color=CARD_BG, corner_radius=15)
        card.grid(row=0, column=0, sticky="nsew")

        # Header with Buttons
        hdr_frame = ctk.CTkFrame(card, fg_color="transparent")
        hdr_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            hdr_frame,
            text="System History (LIFO Stack)",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK,
        ).pack(side="left")
        ctk.CTkButton(
            hdr_frame,
            text="Undo Last Action",
            fg_color=C_DANGER,
            hover_color="#b91c1c",
            height=35,
            command=self._undo,
        ).pack(side="right", padx=(10, 0))
        ctk.CTkButton(
            hdr_frame,
            text="Refresh",
            fg_color=C_BLUE,
            height=35,
            command=self._refresh_history,
        ).pack(side="right")

        tree_container, self.hist_tree = self._create_scrollable_tree(
            card, ("Timestamp", "Action", "Member", "Book"), [160, 90, 220, 360]
        )
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _refresh_history(self):
        self.hist_tree.delete(*self.hist_tree.get_children())
        for entry in self.library.history.to_list():
            self.hist_tree.insert(
                "",
                "end",
                values=(
                    entry["timestamp"],
                    entry["action"],
                    f"{entry['member_name']} ({entry['member_id']})",
                    entry["book_title"],
                ),
            )

    def _undo(self):
        last = self.library.history.peek()
        if last is None:
            messagebox.showinfo("Nothing to undo", "History is empty.")
            return

        confirm = messagebox.askyesno(
            "Confirm Undo",
            f"Undo last action?\n\nAction:  {last['action']}\nMember:  {last['member_name']}\nBook:    {last['book_title']}",
        )
        if not confirm:
            return

        entry = self.library.history.pop()
        if entry is None:
            return

        book = self.library.catalog.find_by_id(entry["book_id"])
        member = self.library.members.find(entry["member_id"])

        if entry["action"] == "BORROW" and book and member:
            book.available += 1
            if entry["book_id"] in member["borrowed"]:
                member["borrowed"].remove(entry["book_id"])
        elif entry["action"] == "RETURN" and book and member:
            if book.available > 0:
                book.available -= 1
            member["borrowed"].append(entry["book_id"])

        self._refresh_history()
        messagebox.showinfo(
            "Undone", f"Action undone: {entry['action']} — {entry['book_title']}"
        )
