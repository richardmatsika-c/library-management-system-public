# gui.py
# ─────────────────────────────────────────────────────────────────────────────
# User Interface Layer (View) - Dark/Teal Modern Design System (Full Card UI)
# ─────────────────────────────────────────────────────────────────────────────

import customtkinter as ctk
from tkinter import simpledialog, messagebox
from controller import Library

# ── DESIGN SYSTEM: Color Palette ──────────────────────────────────────────────
MAIN_BG = "#0F172A"  # Deep slate background
SIDEBAR_BG = "#1E293B"  # Slightly lighter slate for sidebar & cards
CARD_BG = "#1E293B"  # Card background
ITEM_BG = "#334155"  # Input fields & subtle highlights

TEXT_PRIMARY = "#F8FAFC"  # High contrast white for headings/values
TEXT_SECONDARY = "#94A3B8"  # Muted gray for labels/secondary text

ACCENT_TEAL = "#2DD4BF"  # Primary Teal/Cyan accent
ACCENT_HOVER = "#14B8A6"  # Slightly darker teal for hovers
C_DANGER = "#E11D48"  # Muted red for destructive actions
C_WARN = "#D97706"  # Amber for warnings/sorts

RAD_CARD = 12  # Rounded rectangles for cards
RAD_BTN = 20  # Pill-shaped buttons


class ModernLibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.library = Library()

        self.title("Library Management System")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        ctk.set_appearance_mode("dark")
        self.configure(fg_color=MAIN_BG)

        self.frames = {}
        self._build_sidebar()

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(
            side="right", fill="both", expand=True, padx=30, pady=30
        )

        self._build_dashboard()
        self._build_books()
        self._build_members()
        self._build_borrow()
        self._build_search()
        self._build_history()

        self._select_frame("Dashboard")

    # ── ROUTER ────────────────────────────────────────────────────────────────
    def _select_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

        if name == "Dashboard":
            self._refresh_dashboard()
        elif name == "Books":
            self._refresh_books()
        elif name == "Members":
            self._refresh_members()
        elif name == "Borrow / Return":
            self._refresh_queue()
        elif name == "Search":
            self._show_all()
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
            text="Library MS",
            font=("Segoe UI", 24, "bold"),
            text_color=TEXT_PRIMARY,
        ).pack(pady=(35, 40), padx=25, anchor="w")

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
                text=item,
                anchor="w",
                font=("Segoe UI", 13, "bold"),
                fg_color="transparent",
                text_color=TEXT_SECONDARY,
                hover_color=ITEM_BG,
                corner_radius=RAD_CARD,
                height=45,
                command=lambda n=item: self._select_frame(n),
            )
            btn.pack(fill="x", padx=15, pady=4)

    # ── 1. DASHBOARD SCREEN ───────────────────────────────────────────────────
    def _build_dashboard(self):
        dash_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["Dashboard"] = dash_frame

        ctk.CTkLabel(
            dash_frame,
            text="Dashboard Overview",
            font=("Segoe UI", 26, "bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 25))

        self.stats_frame = ctk.CTkFrame(dash_frame, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=(0, 30))
        self.stats_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")

        self.stat_labels = {}
        stat_configs = [
            ("Total Books", "📚", "#3b82f6"),
            ("Active Members", "👥", "#10b981"),
            ("Books Borrowed", "🔖", "#f59e0b"),
            ("Waitlist Queue", "⚠️", "#ef4444"),
        ]

        for i, (title, icon, color) in enumerate(stat_configs):
            card = ctk.CTkFrame(
                self.stats_frame, fg_color=CARD_BG, corner_radius=RAD_CARD, height=110
            )
            card.grid(row=0, column=i, padx=10, sticky="nsew")
            card.pack_propagate(False)
            ctk.CTkLabel(card, text=icon, font=("Segoe UI Emoji", 24)).pack(
                pady=(10, 0)
            )
            val_lbl = ctk.CTkLabel(
                card, text="0", font=("Segoe UI", 28, "bold"), text_color=ACCENT_TEAL
            )
            val_lbl.pack()
            self.stat_labels[title] = val_lbl
            ctk.CTkLabel(
                card, text=title, font=("Segoe UI", 12), text_color=TEXT_SECONDARY
            ).pack()

        ctk.CTkLabel(
            dash_frame,
            text="Recent Transactions",
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", padx=10, pady=(10, 5))
        self.dash_feed_scroll = ctk.CTkScrollableFrame(
            dash_frame, fg_color="transparent"
        )
        self.dash_feed_scroll.pack(fill="both", expand=True, padx=10)

    def _refresh_dashboard(self):
        borrowed_count = sum(len(m["borrowed"]) for m in self.library.members.all())
        self.stat_labels["Total Books"].configure(text=str(self.library.catalog.count))
        self.stat_labels["Active Members"].configure(
            text=str(len(self.library.members.all()))
        )
        self.stat_labels["Books Borrowed"].configure(text=str(borrowed_count))
        self.stat_labels["Waitlist Queue"].configure(
            text=str(self.library.reservations.size())
        )

        for widget in self.dash_feed_scroll.winfo_children():
            widget.destroy()
        for entry in self.library.history.to_list()[:10]:
            self._build_history_card(self.dash_feed_scroll, entry)

    # ── 2. BOOKS SCREEN ───────────────────────────────────────────────────────
    def _build_books(self):
        books_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["Books"] = books_frame

        hdr_frame = ctk.CTkFrame(books_frame, fg_color="transparent")
        hdr_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            hdr_frame,
            text="Book Management",
            font=("Segoe UI", 20, "bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        ctk.CTkButton(
            hdr_frame,
            text="+ Add New",
            fg_color=ACCENT_TEAL,
            hover_color=ACCENT_HOVER,
            text_color=MAIN_BG,
            corner_radius=RAD_BTN,
            height=35,
            command=self._prompt_add_book,
        ).pack(side="right")

        ctk.CTkButton(
            hdr_frame,
            text="Remove",
            fg_color="transparent",
            border_width=1,
            border_color=C_DANGER,
            text_color=C_DANGER,
            hover_color="#4C1D2A",
            corner_radius=RAD_BTN,
            height=35,
            command=self._prompt_remove_book,
        ).pack(side="right", padx=10)

        ctk.CTkButton(
            hdr_frame,
            text="Sort (Merge)",
            fg_color="transparent",
            border_width=1,
            border_color=ITEM_BG,
            text_color=TEXT_SECONDARY,
            hover_color=ITEM_BG,
            corner_radius=RAD_BTN,
            height=35,
            command=self._sort_books,
        ).pack(side="right")

        self.sort_key_var = ctk.StringVar(value="title")
        self.sort_menu = ctk.CTkOptionMenu(
            hdr_frame,
            variable=self.sort_key_var,
            values=["title", "author", "genre"],
            fg_color=ITEM_BG,
            button_color=ITEM_BG,
            button_hover_color=SIDEBAR_BG,
            text_color=TEXT_PRIMARY,
            height=35,
            width=110,
        )
        self.sort_menu.pack(side="right", padx=10)

        self.books_scroll = ctk.CTkScrollableFrame(books_frame, fg_color="transparent")
        self.books_scroll.pack(fill="both", expand=True)

    def _refresh_books(self):
        for widget in self.books_scroll.winfo_children():
            widget.destroy()
        for b in self.library.catalog.to_list():
            self._build_book_card(self.books_scroll, b)

    def _build_book_card(self, parent, b):
        card = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=10, height=75)
        card.pack(fill="x", pady=5)
        card.pack_propagate(False)

        icon_box = ctk.CTkFrame(
            card, fg_color="#132A2F", width=50, height=50, corner_radius=8
        )
        icon_box.pack(side="left", padx=15, pady=12)
        icon_box.pack_propagate(False)
        ctk.CTkLabel(
            icon_box, text="📖", font=("Segoe UI Emoji", 20), text_color=ACCENT_TEAL
        ).pack(expand=True)

        text_frame = ctk.CTkFrame(card, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=12)
        ctk.CTkLabel(
            text_frame,
            text=f"{b.title} (ID: {b.book_id})",
            font=("Segoe UI", 15, "bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w")
        ctk.CTkLabel(
            text_frame,
            text=f"{b.author} • Genre: {b.genre} • Available: {b.available}/{b.copies}",
            font=("Segoe UI", 12),
            text_color=TEXT_SECONDARY,
        ).pack(anchor="w")

        btn_color = ACCENT_TEAL if b.available > 0 else TEXT_SECONDARY
        btn_text = "Checkout" if b.available > 0 else "Waitlist"

        action_btn = ctk.CTkButton(
            card,
            text=btn_text,
            fg_color="transparent",
            border_width=1,
            border_color=btn_color,
            text_color=btn_color,
            hover_color=ITEM_BG,
            corner_radius=RAD_BTN,
            height=32,
            width=90,
        )
        action_btn.pack(side="right", padx=20)
        action_btn.configure(
            command=lambda book_id=b.book_id: self._quick_checkout(book_id)
        )

    def _quick_checkout(self, book_id):
        from tkinter import simpledialog

        member_id = simpledialog.askstring("Checkout", "Enter Member ID:", parent=self)
        if member_id:
            ok, msg = self.library.borrow_book(member_id.strip(), book_id)
            if ok:
                self._refresh_books()
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showwarning("Notice", msg)

    def _prompt_add_book(self):
        from tkinter import simpledialog

        title = simpledialog.askstring("Add Book", "Enter Title:", parent=self)
        if not title:
            return
        author = simpledialog.askstring("Add Book", "Enter Author:", parent=self)
        genre = simpledialog.askstring("Add Book", "Enter Genre:", parent=self)
        copies = simpledialog.askstring("Add Book", "Enter Copies:", parent=self)

        ok, msg = self.library.add_book(title, author, genre, copies)
        messagebox.showinfo("Result", msg)
        self._refresh_books()

    def _prompt_remove_book(self):
        from tkinter import simpledialog

        b_id = simpledialog.askstring(
            "Remove Book", "Enter Book ID to remove:", parent=self
        )
        if b_id:
            ok, msg = self.library.remove_book(b_id)
            messagebox.showinfo("Result", msg)
            self._refresh_books()

    def _sort_books(self):
        selected_key = self.sort_key_var.get()
        self.library.sort_catalog(selected_key)
        self._refresh_books()

    # ── 3. MEMBERS SCREEN ─────────────────────────────────────────────────────
    def _build_members(self):
        mem_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["Members"] = mem_frame

        hdr_frame = ctk.CTkFrame(mem_frame, fg_color="transparent")
        hdr_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(
            hdr_frame,
            text="Member Directory",
            font=("Segoe UI", 20, "bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        ctk.CTkButton(
            hdr_frame,
            text="Remove",
            fg_color="transparent",
            border_width=1,
            border_color=C_DANGER,
            text_color=C_DANGER,
            hover_color="#4C1D2A",
            corner_radius=RAD_BTN,
            height=35,
            command=self._prompt_remove_member,
        ).pack(side="right", padx=10)
        ctk.CTkButton(
            hdr_frame,
            text="+ Add Member",
            fg_color=ACCENT_TEAL,
            hover_color=ACCENT_HOVER,
            text_color=MAIN_BG,
            corner_radius=RAD_BTN,
            height=35,
            command=self._prompt_add_member,
        ).pack(side="right")

        self.members_scroll = ctk.CTkScrollableFrame(mem_frame, fg_color="transparent")
        self.members_scroll.pack(fill="both", expand=True)

    def _refresh_members(self):
        for widget in self.members_scroll.winfo_children():
            widget.destroy()
        for m in self.library.members.all():
            card = ctk.CTkFrame(
                self.members_scroll, fg_color=CARD_BG, corner_radius=10, height=75
            )
            card.pack(fill="x", pady=5)
            card.pack_propagate(False)

            icon_box = ctk.CTkFrame(
                card, fg_color=ITEM_BG, width=50, height=50, corner_radius=8
            )
            icon_box.pack(side="left", padx=15, pady=12)
            icon_box.pack_propagate(False)
            ctk.CTkLabel(
                icon_box, text="👤", font=("Segoe UI Emoji", 20), text_color=ACCENT_TEAL
            ).pack(expand=True)

            text_frame = ctk.CTkFrame(card, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=12)
            ctk.CTkLabel(
                text_frame,
                text=f"{m['name']} (ID: {m['member_id']})",
                font=("Segoe UI", 15, "bold"),
                text_color=TEXT_PRIMARY,
            ).pack(anchor="w")
            ctk.CTkLabel(
                text_frame,
                text=f"{m['email']} • {m['phone']} • Joined: {m['joined']}",
                font=("Segoe UI", 12),
                text_color=TEXT_SECONDARY,
            ).pack(anchor="w")

            badge = ctk.CTkFrame(card, fg_color=ITEM_BG, corner_radius=8)
            badge.pack(side="right", padx=20)
            ctk.CTkLabel(
                badge,
                text=f"Borrowed: {len(m['borrowed'])}",
                font=("Segoe UI", 12, "bold"),
                text_color=ACCENT_TEAL,
            ).pack(padx=12, pady=6)

    def _prompt_add_member(self):
        name = simpledialog.askstring("Add Member", "Enter Full Name:", parent=self)
        if not name:
            return
        email = simpledialog.askstring("Add Member", "Enter Email:", parent=self)
        phone = simpledialog.askstring("Add Member", "Enter Phone:", parent=self)
        ok, msg = self.library.add_member(name, email, phone)
        messagebox.showinfo("Result", msg)
        self._refresh_members()

    def _prompt_remove_member(self):
        m_id = simpledialog.askstring("Remove Member", "Enter Member ID:", parent=self)
        if m_id:
            ok, msg = self.library.remove_member(m_id)
            messagebox.showinfo("Result", msg)
            self._refresh_members()

    # ── 4. BORROW / RETURN SCREEN ─────────────────────────────────────────────
    def _build_borrow(self):
        br_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["Borrow / Return"] = br_frame
        br_frame.columnconfigure((0, 1), weight=1)
        br_frame.rowconfigure(1, weight=1)

        borrow_card = ctk.CTkFrame(br_frame, fg_color=CARD_BG, corner_radius=RAD_CARD)
        borrow_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 20))
        ctk.CTkLabel(
            borrow_card,
            text="Checkout Book",
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", padx=20, pady=20)

        input_frame = ctk.CTkFrame(borrow_card, fg_color="transparent")
        input_frame.pack(fill="x", padx=20)
        self.br_member = ctk.CTkEntry(
            input_frame,
            placeholder_text="Member ID",
            width=140,
            height=40,
            fg_color=ITEM_BG,
            border_width=0,
        )
        self.br_member.pack(side="left", padx=(0, 10), expand=True, fill="x")
        self.br_book = ctk.CTkEntry(
            input_frame,
            placeholder_text="Book ID",
            width=140,
            height=40,
            fg_color=ITEM_BG,
            border_width=0,
        )
        self.br_book.pack(side="left", padx=(0, 10), expand=True, fill="x")
        ctk.CTkButton(
            input_frame,
            text="Checkout",
            fg_color=ACCENT_TEAL,
            text_color=MAIN_BG,
            corner_radius=RAD_BTN,
            font=("Segoe UI", 13, "bold"),
            width=100,
            height=40,
            command=self._borrow,
        ).pack(side="right")

        return_card = ctk.CTkFrame(br_frame, fg_color=CARD_BG, corner_radius=RAD_CARD)
        return_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 20))
        ctk.CTkLabel(
            return_card,
            text="Return Book",
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", padx=20, pady=20)

        ret_input_frame = ctk.CTkFrame(return_card, fg_color="transparent")
        ret_input_frame.pack(fill="x", padx=20)
        self.rt_member = ctk.CTkEntry(
            ret_input_frame,
            placeholder_text="Member ID",
            width=140,
            height=40,
            fg_color=ITEM_BG,
            border_width=0,
        )
        self.rt_member.pack(side="left", padx=(0, 10), expand=True, fill="x")
        self.rt_book = ctk.CTkEntry(
            ret_input_frame,
            placeholder_text="Book ID",
            width=140,
            height=40,
            fg_color=ITEM_BG,
            border_width=0,
        )
        self.rt_book.pack(side="left", padx=(0, 10), expand=True, fill="x")
        ctk.CTkButton(
            ret_input_frame,
            text="Return",
            fg_color="transparent",
            border_width=1,
            border_color=ACCENT_TEAL,
            text_color=ACCENT_TEAL,
            hover_color=ITEM_BG,
            corner_radius=RAD_BTN,
            font=("Segoe UI", 13, "bold"),
            width=100,
            height=40,
            command=self._return,
        ).pack(side="right")

        queue_hdr = ctk.CTkFrame(br_frame, fg_color="transparent")
        queue_hdr.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))
        ctk.CTkLabel(
            queue_hdr,
            text="Reservation Waitlist (FIFO)",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        self.queue_scroll = ctk.CTkScrollableFrame(br_frame, fg_color="transparent")
        self.queue_scroll.grid(row=2, column=0, columnspan=2, sticky="nsew")

    def _refresh_queue(self):
        for widget in self.queue_scroll.winfo_children():
            widget.destroy()
        for i, e in enumerate(self.library.reservations.to_list(), 1):
            card = ctk.CTkFrame(
                self.queue_scroll, fg_color=CARD_BG, corner_radius=10, height=70
            )
            card.pack(fill="x", pady=4)
            card.pack_propagate(False)

            icon_box = ctk.CTkFrame(
                card, fg_color=ITEM_BG, width=45, height=45, corner_radius=8
            )
            icon_box.pack(side="left", padx=15, pady=12)
            icon_box.pack_propagate(False)
            ctk.CTkLabel(
                icon_box, text="⏳", font=("Segoe UI Emoji", 18), text_color=C_WARN
            ).pack(expand=True)

            text_frame = ctk.CTkFrame(card, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=12)
            ctk.CTkLabel(
                text_frame,
                text=f"{e['member_name']} (ID: {e['member_id']}) — Waiting for: {e['book_title']}",
                font=("Segoe UI", 14, "bold"),
                text_color=TEXT_PRIMARY,
            ).pack(anchor="w")
            ctk.CTkLabel(
                text_frame,
                text=f"Queued At: {e['timestamp']}",
                font=("Segoe UI", 11),
                text_color=TEXT_SECONDARY,
            ).pack(anchor="w")

            badge = ctk.CTkFrame(card, fg_color=ITEM_BG, corner_radius=8)
            badge.pack(side="right", padx=20)
            ctk.CTkLabel(
                badge,
                text=f"Rank #{i}",
                font=("Segoe UI", 12, "bold"),
                text_color=C_WARN,
            ).pack(padx=12, pady=6)

    def _borrow(self):
        ok, msg = self.library.borrow_book(
            self.br_member.get().strip(), self.br_book.get().strip()
        )
        if ok:
            self.br_member.delete(0, "end")
            self.br_book.delete(0, "end")
            self._refresh_queue()
        else:
            self._refresh_queue()
            messagebox.showwarning("Notice", msg)

    def _return(self):
        ok, msg = self.library.return_book(
            self.rt_member.get().strip(), self.rt_book.get().strip()
        )
        if ok:
            self.rt_member.delete(0, "end")
            self.rt_book.delete(0, "end")
            self._refresh_queue()
        else:
            messagebox.showerror("Error", msg)

    # ── 5. SEARCH SCREEN ──────────────────────────────────────────────────────
    def _build_search(self):
        search_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["Search"] = search_frame
        search_frame.columnconfigure(0, weight=1)
        search_frame.rowconfigure(1, weight=1)

        bar_card = ctk.CTkFrame(search_frame, fg_color=CARD_BG, corner_radius=RAD_CARD)
        bar_card.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        controls_frame = ctk.CTkFrame(bar_card, fg_color="transparent")
        controls_frame.pack(fill="x", padx=20, pady=20)

        self.search_var = ctk.StringVar()
        se = ctk.CTkEntry(
            controls_frame,
            textvariable=self.search_var,
            placeholder_text="Search catalog...",
            height=40,
            width=400,
            fg_color=ITEM_BG,
            border_width=0,
        )
        se.pack(side="left", padx=(0, 15))
        se.bind("<Return>", lambda e: self._do_search())

        self.search_field = ctk.CTkOptionMenu(
            controls_frame,
            values=["title", "author", "genre"],
            height=40,
            fg_color=ITEM_BG,
            button_color=ITEM_BG,
        )
        self.search_field.pack(side="left", padx=(0, 15))

        ctk.CTkButton(
            controls_frame,
            text="Search",
            fg_color=ACCENT_TEAL,
            text_color=MAIN_BG,
            font=("Segoe UI", 13, "bold"),
            corner_radius=RAD_BTN,
            height=40,
            command=self._do_search,
        ).pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            controls_frame,
            text="Clear",
            fg_color="transparent",
            border_width=1,
            border_color=TEXT_SECONDARY,
            text_color=TEXT_SECONDARY,
            hover_color=ITEM_BG,
            font=("Segoe UI", 13, "bold"),
            corner_radius=RAD_BTN,
            height=40,
            command=self._show_all,
        ).pack(side="left")

        hdr_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        hdr_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 5))
        ctk.CTkLabel(
            hdr_frame,
            text="Search Results",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        self.search_scroll = ctk.CTkScrollableFrame(
            search_frame, fg_color="transparent"
        )
        self.search_scroll.grid(row=2, column=0, sticky="nsew")

    def _do_search(self):
        query = self.search_var.get().strip()
        results = self.library.search(query, self.search_field.get())
        for widget in self.search_scroll.winfo_children():
            widget.destroy()
        for b in results:
            self._build_book_card(self.search_scroll, b)

    def _show_all(self):
        self.search_var.set("")
        for widget in self.search_scroll.winfo_children():
            widget.destroy()
        for b in self.library.catalog.to_list():
            self._build_book_card(self.search_scroll, b)

    # ── 6. HISTORY SCREEN ─────────────────────────────────────────────────────
    def _build_history(self):
        hist_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["History"] = hist_frame
        hist_frame.columnconfigure(0, weight=1)
        hist_frame.rowconfigure(1, weight=1)

        hdr_frame = ctk.CTkFrame(hist_frame, fg_color="transparent")
        hdr_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(
            hdr_frame,
            text="Activity Log (Stack)",
            font=("Segoe UI", 20, "bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left")
        ctk.CTkButton(
            hdr_frame,
            text="Undo Last",
            fg_color="transparent",
            border_width=1,
            border_color=C_DANGER,
            text_color=C_DANGER,
            hover_color="#4C1D2A",
            corner_radius=RAD_BTN,
            font=("Segoe UI", 12, "bold"),
            height=35,
            command=self._undo,
        ).pack(side="right", padx=(10, 0))

        self.hist_scroll = ctk.CTkScrollableFrame(hist_frame, fg_color="transparent")
        self.hist_scroll.grid(row=1, column=0, sticky="nsew")

    def _build_history_card(self, parent, entry):
        is_borrow = entry["action"] == "BORROW"
        card_color = CARD_BG
        icon = "📤" if is_borrow else "📥"
        accent = C_WARN if is_borrow else ACCENT_TEAL

        card = ctk.CTkFrame(parent, fg_color=card_color, corner_radius=8, height=65)
        card.pack(fill="x", pady=4)
        card.pack_propagate(False)

        icon_box = ctk.CTkFrame(
            card, fg_color=ITEM_BG, width=40, height=40, corner_radius=8
        )
        icon_box.pack(side="left", padx=15, pady=12)
        icon_box.pack_propagate(False)
        ctk.CTkLabel(
            icon_box, text=icon, font=("Segoe UI Emoji", 16), text_color=accent
        ).pack(expand=True)

        text_frame = ctk.CTkFrame(card, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        title_text = (
            f"{entry['member_name']} ({entry['member_id']}) — {entry['book_title']}"
        )
        ctk.CTkLabel(
            text_frame,
            text=title_text,
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w")
        ctk.CTkLabel(
            text_frame,
            text=f"{entry['timestamp']}",
            font=("Segoe UI", 11),
            text_color=TEXT_SECONDARY,
        ).pack(anchor="w")

        badge = ctk.CTkFrame(card, fg_color=accent, corner_radius=4)
        badge.pack(side="right", padx=20)
        ctk.CTkLabel(
            badge,
            text=entry["action"],
            font=("Segoe UI", 11, "bold"),
            text_color=MAIN_BG,
        ).pack(padx=10, pady=4)

    def _refresh_history(self):
        for widget in self.hist_scroll.winfo_children():
            widget.destroy()
        for entry in self.library.history.to_list():
            self._build_history_card(self.hist_scroll, entry)

    def _undo(self):
        last = self.library.history.peek()
        if not last:
            return
        confirm = messagebox.askyesno(
            "Confirm Undo",
            f"Reverse this action?\n\n{last['action']}: {last['book_title']}",
        )
        if not confirm:
            return

        entry = self.library.history.pop()
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
