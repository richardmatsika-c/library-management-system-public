# gui.py
# ─────────────────────────────────────────────────────────────────────────────
# User Interface Layer (View)
# ─────────────────────────────────────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk, messagebox
from controller import Library

# ── Colour palette ────────────────────────────────────────────────────────────
BG = "#1E2235"
CARD = "#272D45"
ACCENT = "#4A9EFF"
SUCCESS = "#3ECF8E"
WARNING = "#F6AD55"
DANGER = "#FC5C7D"
TEXT = "#E8EAF0"
SUBTEXT = "#8892A4"
BORDER = "#3A4260"
WHITE = "#FFFFFF"
HDR_BG = "#141826"


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.library = Library()
        self.title("Library Management System — CUITM205")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=CARD,
            foreground=SUBTEXT,
            padding=[18, 8],
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", ACCENT)],
            foreground=[("selected", WHITE)],
        )

        style.configure("TFrame", background=BG)
        style.configure("Card.TFrame", background=CARD, relief="flat")
        style.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 10))
        style.configure(
            "Card.TLabel", background=CARD, foreground=TEXT, font=("Segoe UI", 10)
        )
        style.configure(
            "Header.TLabel",
            background=HDR_BG,
            foreground=WHITE,
            font=("Segoe UI", 16, "bold"),
        )
        style.configure(
            "Sub.TLabel", background=CARD, foreground=SUBTEXT, font=("Segoe UI", 9)
        )

        style.configure(
            "Accent.TButton",
            background=ACCENT,
            foreground=WHITE,
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            padding=[12, 6],
        )
        style.map("Accent.TButton", background=[("active", "#3A8EEF")])

        style.configure(
            "Success.TButton",
            background=SUCCESS,
            foreground=WHITE,
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            padding=[12, 6],
        )
        style.map("Success.TButton", background=[("active", "#2EBF7E")])

        style.configure(
            "Danger.TButton",
            background=DANGER,
            foreground=WHITE,
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            padding=[12, 6],
        )
        style.map("Danger.TButton", background=[("active", "#EC4C6D")])

        style.configure(
            "Warning.TButton",
            background=WARNING,
            foreground=WHITE,
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            padding=[12, 6],
        )
        style.map("Warning.TButton", background=[("active", "#E69945")])

        style.configure(
            "Treeview",
            background=CARD,
            foreground=TEXT,
            fieldbackground=CARD,
            rowheight=28,
            font=("Segoe UI", 10),
            borderwidth=0,
        )
        style.configure(
            "Treeview.Heading",
            background=HDR_BG,
            foreground=ACCENT,
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
        )
        style.map(
            "Treeview",
            background=[("selected", ACCENT)],
            foreground=[("selected", WHITE)],
        )

        style.configure(
            "TEntry",
            fieldbackground="#2E3655",
            foreground=TEXT,
            insertbackground=TEXT,
            font=("Segoe UI", 10),
            borderwidth=1,
            relief="flat",
            padding=[6, 4],
        )
        style.configure(
            "TCombobox",
            fieldbackground="#2E3655",
            foreground=TEXT,
            font=("Segoe UI", 10),
        )

        style.configure("TSeparator", background=BORDER)

    def _build_ui(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(
            hdr,
            text="📚  Library Management System",
            bg=HDR_BG,
            fg=WHITE,
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left", padx=24, pady=14)
        tk.Label(
            hdr,
            text="CUITM205 — Data Structures & Algorithms",
            bg=HDR_BG,
            fg=SUBTEXT,
            font=("Segoe UI", 10),
        ).pack(side="right", padx=24)

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=0, pady=0)

        self.tab_dashboard = ttk.Frame(nb)
        self.tab_books = ttk.Frame(nb)
        self.tab_members = ttk.Frame(nb)
        self.tab_borrow = ttk.Frame(nb)
        self.tab_search = ttk.Frame(nb)
        self.tab_history = ttk.Frame(nb)

        nb.add(self.tab_dashboard, text="  Dashboard  ")
        nb.add(self.tab_books, text="  Books  ")
        nb.add(self.tab_members, text="  Members  ")
        nb.add(self.tab_borrow, text="  Borrow / Return  ")
        nb.add(self.tab_search, text="  Search  ")
        nb.add(self.tab_history, text="  History  ")

        self._build_dashboard()
        self._build_books_tab()
        self._build_members_tab()
        self._build_borrow_tab()
        self._build_search_tab()
        self._build_history_tab()

        nb.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _lbl_entry(self, parent, label, row, col=0, width=22):
        ttk.Label(parent, text=label, style="Card.TLabel").grid(
            row=row, column=col, sticky="w", padx=(12, 4), pady=4
        )
        var = tk.StringVar()
        e = ttk.Entry(parent, textvariable=var, width=width)
        e.grid(row=row, column=col + 1, sticky="ew", padx=(0, 12), pady=4)
        return var

    def _card(self, parent, title, row=0, col=0, rowspan=1, colspan=1, padx=8, pady=8):
        f = tk.Frame(parent, bg=CARD, bd=0, relief="flat")
        f.grid(
            row=row,
            column=col,
            rowspan=rowspan,
            columnspan=colspan,
            sticky="nsew",
            padx=padx,
            pady=pady,
        )

        tk.Label(f, text=title, bg=CARD, fg=ACCENT, font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=12, pady=(10, 4)
        )
        tk.Frame(f, bg=BORDER, height=1).pack(fill="x", padx=12)

        content_frame = tk.Frame(f, bg=CARD, bd=0)
        content_frame.pack(fill="both", expand=True)

        return content_frame

    def _build_dashboard(self):
        tab = self.tab_dashboard
        tab.configure(style="TFrame")
        tab.columnconfigure((0, 1, 2, 3), weight=1)
        tab.rowconfigure(1, weight=1)

        stats = [
            ("Total Books", str(self.library.catalog.count), ACCENT),
            ("Registered Members", str(len(self.library.members.all())), SUCCESS),
            ("Books Borrowed", "0", WARNING),
            ("Queue Reservations", str(self.library.reservations.size()), DANGER),
        ]
        self._stat_vars = []
        for i, (label, value, color) in enumerate(stats):
            f = tk.Frame(tab, bg=CARD, bd=0)
            f.grid(row=0, column=i, sticky="nsew", padx=10, pady=(14, 6))
            tk.Label(
                f, text=value, bg=CARD, fg=color, font=("Segoe UI", 36, "bold")
            ).pack(pady=(14, 2))
            tk.Label(f, text=label, bg=CARD, fg=SUBTEXT, font=("Segoe UI", 10)).pack(
                pady=(0, 14)
            )
            var = tk.StringVar(value=value)
            self._stat_vars.append((var, color, label))

        feed_card = self._card(tab, "Recent Activity", row=1, col=0, colspan=4)
        self.feed_tree = ttk.Treeview(
            feed_card,
            columns=("time", "action", "member", "book"),
            show="headings",
            height=12,
        )
        for col, hdr, w in [
            ("time", "Time", 160),
            ("action", "Action", 100),
            ("member", "Member", 180),
            ("book", "Book", 340),
        ]:
            self.feed_tree.heading(col, text=hdr)
            self.feed_tree.column(col, width=w, anchor="w")
        sb = ttk.Scrollbar(feed_card, orient="vertical", command=self.feed_tree.yview)
        self.feed_tree.configure(yscrollcommand=sb.set)
        self.feed_tree.pack(side="left", fill="both", expand=True, padx=12, pady=8)
        sb.pack(side="right", fill="y", pady=8)

    def _refresh_dashboard(self):
        borrowed_count = sum(len(m["borrowed"]) for m in self.library.members.all())
        new_stats = [
            self.library.catalog.count,
            len(self.library.members.all()),
            borrowed_count,
            self.library.reservations.size(),
        ]
        tab = self.tab_dashboard
        for widget in tab.winfo_children():
            info = widget.grid_info()  # type: ignore
            if info.get("row") == "0":
                widget.destroy()
        colors = [ACCENT, SUCCESS, WARNING, DANGER]
        labels = [
            "Total Books",
            "Registered Members",
            "Books Borrowed",
            "Queue Reservations",
        ]
        for i, (value, color, label) in enumerate(zip(new_stats, colors, labels)):
            f = tk.Frame(tab, bg=CARD, bd=0)
            f.grid(row=0, column=i, sticky="nsew", padx=10, pady=(14, 6))
            tk.Label(
                f, text=str(value), bg=CARD, fg=color, font=("Segoe UI", 36, "bold")
            ).pack(pady=(14, 2))
            tk.Label(f, text=label, bg=CARD, fg=SUBTEXT, font=("Segoe UI", 10)).pack(
                pady=(0, 14)
            )

        self.feed_tree.delete(*self.feed_tree.get_children())
        for entry in self.library.history.to_list():
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

    def _build_books_tab(self):
        tab = self.tab_books
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=3)
        tab.rowconfigure(0, weight=1)

        left = self._card(tab, "Add New Book", row=0, col=0)
        left.columnconfigure(1, weight=1)

        self.bk_title = self._lbl_entry(left, "Title *", 1)
        self.bk_author = self._lbl_entry(left, "Author *", 2)
        self.bk_genre = self._lbl_entry(left, "Genre", 3)
        self.bk_copies = self._lbl_entry(left, "Copies *", 4, width=8)
        self.bk_copies.set("1")

        ttk.Button(
            left, text="Add Book", style="Accent.TButton", command=self._add_book
        ).grid(row=5, column=0, columnspan=2, padx=12, pady=12, sticky="ew")

        ttk.Separator(left, orient="horizontal").grid(
            row=6, column=0, columnspan=2, sticky="ew", padx=12, pady=4
        )

        tk.Label(
            left, text="Remove Book", bg=CARD, fg=ACCENT, font=("Segoe UI", 11, "bold")
        ).grid(row=7, column=0, columnspan=2, sticky="w", padx=12, pady=(8, 4))

        self.bk_del_id = self._lbl_entry(left, "Book ID", 8, width=10)
        ttk.Button(
            left, text="Remove Book", style="Danger.TButton", command=self._remove_book
        ).grid(row=9, column=0, columnspan=2, padx=12, pady=8, sticky="ew")

        ttk.Separator(left, orient="horizontal").grid(
            row=10, column=0, columnspan=2, sticky="ew", padx=12, pady=4
        )

        tk.Label(
            left, text="Sort Catalog", bg=CARD, fg=ACCENT, font=("Segoe UI", 11, "bold")
        ).grid(row=11, column=0, columnspan=2, sticky="w", padx=12, pady=(8, 4))

        tk.Label(left, text="Sort by:", bg=CARD, fg=TEXT, font=("Segoe UI", 10)).grid(
            row=12, column=0, sticky="w", padx=12
        )
        self.sort_key = ttk.Combobox(
            left, values=["title", "author", "genre"], state="readonly", width=12
        )
        self.sort_key.set("title")
        self.sort_key.grid(row=12, column=1, sticky="w", padx=4, pady=4)

        ttk.Button(
            left,
            text="Sort (Merge Sort)",
            style="Warning.TButton",
            command=self._sort_books,
        ).grid(row=13, column=0, columnspan=2, padx=12, pady=8, sticky="ew")

        right = self._card(tab, "Book Catalog", row=0, col=1)

        cols = ("ID", "Title", "Author", "Genre", "Copies", "Available")
        self.books_tree = ttk.Treeview(right, columns=cols, show="headings", height=20)
        widths = [60, 280, 160, 130, 70, 80]
        for col, w in zip(cols, widths):
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=w, anchor="w")
        sb2 = ttk.Scrollbar(right, orient="vertical", command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=sb2.set)
        self.books_tree.pack(side="left", fill="both", expand=True, padx=12, pady=8)
        sb2.pack(side="right", fill="y", pady=8)

        self._refresh_books()

    def _refresh_books(self):
        self.books_tree.delete(*self.books_tree.get_children())
        for b in self.library.catalog.to_list():
            avail_tag = (
                "low"
                if b.available == 0
                else ("ok" if b.available == b.copies else "partial")
            )
            self.books_tree.insert(
                "",
                "end",
                values=(b.book_id, b.title, b.author, b.genre, b.copies, b.available),
                tags=(avail_tag,),
            )
        self.books_tree.tag_configure("low", foreground=DANGER)
        self.books_tree.tag_configure("partial", foreground=WARNING)
        self.books_tree.tag_configure("ok", foreground=SUCCESS)

    def _add_book(self):
        ok, msg = self.library.add_book(
            self.bk_title.get().strip(),
            self.bk_author.get().strip(),
            self.bk_genre.get().strip(),
            self.bk_copies.get().strip(),
        )
        if ok:
            for v in [self.bk_title, self.bk_author, self.bk_genre]:
                v.set("")
            self.bk_copies.set("1")
            self._refresh_books()
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    def _remove_book(self):
        ok, msg = self.library.remove_book(self.bk_del_id.get().strip())
        if ok:
            self.bk_del_id.set("")
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

    def _build_members_tab(self):
        tab = self.tab_members
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=3)
        tab.rowconfigure(0, weight=1)

        left = self._card(tab, "Register New Member", row=0, col=0)
        left.columnconfigure(1, weight=1)

        self.mb_name = self._lbl_entry(left, "Full Name *", 1)
        self.mb_email = self._lbl_entry(left, "Email", 2)
        self.mb_phone = self._lbl_entry(left, "Phone", 3)

        ttk.Button(
            left,
            text="Register Member",
            style="Success.TButton",
            command=self._add_member,
        ).grid(row=4, column=0, columnspan=2, padx=12, pady=12, sticky="ew")

        ttk.Separator(left).grid(
            row=5, column=0, columnspan=2, sticky="ew", padx=12, pady=4
        )

        tk.Label(
            left,
            text="Remove Member",
            bg=CARD,
            fg=ACCENT,
            font=("Segoe UI", 11, "bold"),
        ).grid(row=6, column=0, columnspan=2, sticky="w", padx=12, pady=(8, 4))

        self.mb_del_id = self._lbl_entry(left, "Member ID", 7, width=10)
        ttk.Button(
            left,
            text="Remove Member",
            style="Danger.TButton",
            command=self._remove_member,
        ).grid(row=8, column=0, columnspan=2, padx=12, pady=8, sticky="ew")

        right = self._card(tab, "Member Directory", row=0, col=1)
        cols = ("ID", "Name", "Email", "Phone", "Borrowed", "Joined")
        self.members_tree = ttk.Treeview(
            right, columns=cols, show="headings", height=20
        )
        for col, w in zip(cols, [80, 200, 200, 130, 90, 100]):
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=w, anchor="w")
        sb = ttk.Scrollbar(right, orient="vertical", command=self.members_tree.yview)
        self.members_tree.configure(yscrollcommand=sb.set)
        self.members_tree.pack(side="left", fill="both", expand=True, padx=12, pady=8)
        sb.pack(side="right", fill="y", pady=8)

        self._refresh_members()

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
                v.set("")
            self._refresh_members()
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    def _remove_member(self):
        ok, msg = self.library.remove_member(self.mb_del_id.get().strip())
        if ok:
            self.mb_del_id.set("")
            self._refresh_members()
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    def _build_borrow_tab(self):
        tab = self.tab_borrow
        tab.columnconfigure((0, 1), weight=1)
        tab.rowconfigure(1, weight=1)

        borrow = self._card(tab, "Borrow a Book", row=0, col=0)
        borrow.columnconfigure(1, weight=1)
        self.br_member = self._lbl_entry(borrow, "Member ID *", 1, width=14)
        self.br_book = self._lbl_entry(borrow, "Book ID *", 2, width=14)
        ttk.Button(
            borrow, text="Borrow Book", style="Accent.TButton", command=self._borrow
        ).grid(row=3, column=0, columnspan=2, padx=12, pady=12, sticky="ew")

        ret = self._card(tab, "Return a Book", row=0, col=1)
        ret.columnconfigure(1, weight=1)
        self.rt_member = self._lbl_entry(ret, "Member ID *", 1, width=14)
        self.rt_book = self._lbl_entry(ret, "Book ID *", 2, width=14)
        ttk.Button(
            ret, text="Return Book", style="Success.TButton", command=self._return
        ).grid(row=3, column=0, columnspan=2, padx=12, pady=12, sticky="ew")

        queue_card = self._card(
            tab, "Reservation Queue  (FIFO)", row=1, col=0, colspan=2
        )
        cols = ("#", "Member ID", "Member Name", "Book ID", "Book Title", "Queued At")
        self.queue_tree = ttk.Treeview(
            queue_card, columns=cols, show="headings", height=12
        )
        for col, w in zip(cols, [40, 90, 180, 80, 300, 140]):
            self.queue_tree.heading(col, text=col)
            self.queue_tree.column(col, width=w, anchor="w")
        sb = ttk.Scrollbar(queue_card, orient="vertical", command=self.queue_tree.yview)
        self.queue_tree.configure(yscrollcommand=sb.set)
        self.queue_tree.pack(side="left", fill="both", expand=True, padx=12, pady=8)
        sb.pack(side="right", fill="y", pady=8)
        self._refresh_queue()

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
            self.br_member.set("")
            self.br_book.set("")
            self._refresh_books()
            self._refresh_members()
            self._refresh_queue()
            self._refresh_dashboard()
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showwarning("Notice", msg)

    def _return(self):
        ok, msg = self.library.return_book(
            self.rt_member.get().strip(), self.rt_book.get().strip()
        )
        if ok:
            self.rt_member.set("")
            self.rt_book.set("")
            self._refresh_books()
            self._refresh_members()
            self._refresh_queue()
            self._refresh_dashboard()
            self._refresh_history()
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    def _build_search_tab(self):
        tab = self.tab_search
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

        bar = tk.Frame(tab, bg=CARD)
        bar.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        bar.columnconfigure(1, weight=1)

        tk.Label(
            bar, text="Search:", bg=CARD, fg=TEXT, font=("Segoe UI", 11, "bold")
        ).grid(row=0, column=0, padx=(12, 8), pady=14)
        self.search_var = tk.StringVar()
        se = ttk.Entry(bar, textvariable=self.search_var, width=40)
        se.grid(row=0, column=1, sticky="ew", padx=4, pady=14)
        se.bind("<Return>", lambda e: self._do_search())

        tk.Label(bar, text="Field:", bg=CARD, fg=TEXT, font=("Segoe UI", 10)).grid(
            row=0, column=2, padx=(12, 4)
        )
        self.search_field = ttk.Combobox(
            bar, values=["title", "author", "genre"], state="readonly", width=10
        )
        self.search_field.set("title")
        self.search_field.grid(row=0, column=3, padx=4, pady=14)

        ttk.Button(
            bar,
            text="Search  (Linear Search)",
            style="Accent.TButton",
            command=self._do_search,
        ).grid(row=0, column=4, padx=12, pady=14)
        ttk.Button(
            bar, text="Show All", style="Warning.TButton", command=self._show_all
        ).grid(row=0, column=5, padx=(0, 12), pady=14)

        res_card = self._card(tab, "Search Results", row=1, col=0)
        cols = ("ID", "Title", "Author", "Genre", "Copies", "Available")
        self.search_tree = ttk.Treeview(
            res_card, columns=cols, show="headings", height=20
        )
        for col, w in zip(cols, [60, 300, 180, 130, 70, 80]):
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=w, anchor="w")
        sb = ttk.Scrollbar(res_card, orient="vertical", command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=sb.set)
        self.search_tree.pack(side="left", fill="both", expand=True, padx=12, pady=8)
        sb.pack(side="right", fill="y", pady=8)
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

    def _build_history_tab(self):
        tab = self.tab_history
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)

        card = self._card(
            tab, "Borrow / Return History  (Stack — most recent first)", row=0, col=0
        )

        btn_frame = tk.Frame(card, bg=CARD)
        btn_frame.pack(anchor="e", padx=12, pady=(4, 0))
        ttk.Button(
            btn_frame,
            text="Undo Last Action",
            style="Danger.TButton",
            command=self._undo,
        ).pack(side="right", padx=4)
        ttk.Button(
            btn_frame,
            text="Refresh",
            style="Accent.TButton",
            command=self._refresh_history,
        ).pack(side="right", padx=4)

        cols = ("Timestamp", "Action", "Member", "Book")
        self.hist_tree = ttk.Treeview(card, columns=cols, show="headings", height=22)
        for col, w in zip(cols, [160, 90, 220, 360]):
            self.hist_tree.heading(col, text=col)
            self.hist_tree.column(col, width=w, anchor="w")
        sb = ttk.Scrollbar(card, orient="vertical", command=self.hist_tree.yview)
        self.hist_tree.configure(yscrollcommand=sb.set)
        self.hist_tree.pack(side="left", fill="both", expand=True, padx=12, pady=8)
        sb.pack(side="right", fill="y", pady=8)

    def _refresh_history(self):
        self.hist_tree.delete(*self.hist_tree.get_children())
        for entry in self.library.history.to_list():
            tag = "borrow" if entry["action"] == "BORROW" else "ret"
            self.hist_tree.insert(
                "",
                "end",
                values=(
                    entry["timestamp"],
                    entry["action"],
                    f"{entry['member_name']} ({entry['member_id']})",
                    entry["book_title"],
                ),
                tags=(tag,),
            )
        self.hist_tree.tag_configure("borrow", foreground=WARNING)
        self.hist_tree.tag_configure("ret", foreground=SUCCESS)

    def _undo(self):
        last = self.library.history.peek()
        if last is None:
            messagebox.showinfo("Nothing to undo", "History is empty.")
            return

        confirm = messagebox.askyesno(
            "Confirm Undo",
            f"Undo last action?\n\n"
            f"Action:  {last['action']}\n"
            f"Member:  {last['member_name']}\n"
            f"Book:    {last['book_title']}\n"
            f"Time:    {last['timestamp']}",
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
        self._refresh_books()
        self._refresh_members()
        self._refresh_dashboard()
        messagebox.showinfo(
            "Undone", f"Action undone: {entry['action']} — {entry['book_title']}"
        )

    def _on_tab_change(self, event):
        tab = event.widget.tab(event.widget.select(), "text").strip()
        if tab == "Dashboard":
            self._refresh_dashboard()
        elif tab == "History":
            self._refresh_history()
        elif tab == "Borrow / Return":
            self._refresh_queue()
