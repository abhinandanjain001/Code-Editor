"""
PyCode Studio - A lightweight VS Code-like editor for C, C++, and Java
Built with Python's tkinter library
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import re
import os
import subprocess
import threading
import time
from pathlib import Path


# ──────────────────────────────────────────────
#  THEME DEFINITIONS
# ──────────────────────────────────────────────

THEMES = {
    "dark": {
        "bg":           "#1e1e2e",
        "bg2":          "#181825",
        "bg3":          "#313244",
        "fg":           "#cdd6f4",
        "fg2":          "#a6adc8",
        "accent":       "#89b4fa",
        "accent2":      "#74c7ec",
        "green":        "#a6e3a1",
        "red":          "#f38ba8",
        "yellow":       "#f9e2af",
        "orange":       "#fab387",
        "purple":       "#cba6f7",
        "teal":         "#94e2d5",
        "pink":         "#f5c2e7",
        "line_bg":      "#181825",
        "line_fg":      "#6c7086",
        "select_bg":    "#45475a",
        "cursor":       "#f5e0dc",
        "border":       "#45475a",
        "toolbar_bg":   "#11111b",
        "tab_active":   "#1e1e2e",
        "tab_inactive": "#11111b",
        "console_bg":   "#11111b",
        "console_fg":   "#a6e3a1",
        "error_fg":     "#f38ba8",
        "warning_fg":   "#f9e2af",
        "scrollbar":    "#45475a",
    },
    "light": {
        "bg":           "#eff1f5",
        "bg2":          "#e6e9ef",
        "bg3":          "#dce0e8",
        "fg":           "#4c4f69",
        "fg2":          "#6c6f85",
        "accent":       "#1e66f5",
        "accent2":      "#04a5e5",
        "green":        "#40a02b",
        "red":          "#d20f39",
        "yellow":       "#df8e1d",
        "orange":       "#fe640b",
        "purple":       "#8839ef",
        "teal":         "#179299",
        "pink":         "#ea76cb",
        "line_bg":      "#e6e9ef",
        "line_fg":      "#9ca0b0",
        "select_bg":    "#ccd0da",
        "cursor":       "#dc8a78",
        "border":       "#ccd0da",
        "toolbar_bg":   "#dce0e8",
        "tab_active":   "#eff1f5",
        "tab_inactive": "#e6e9ef",
        "console_bg":   "#dce0e8",
        "console_fg":   "#40a02b",
        "error_fg":     "#d20f39",
        "warning_fg":   "#df8e1d",
        "scrollbar":    "#ccd0da",
    }
}

# ──────────────────────────────────────────────
#  SYNTAX HIGHLIGHT RULES
# ──────────────────────────────────────────────

SYNTAX = {
    "c": {
        "keywords": (
            r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|'
            r'extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|'
            r'static|struct|switch|typedef|union|unsigned|void|volatile|while|'
            r'NULL|true|false|bool|include|define|ifdef|ifndef|endif|pragma)\b'
        ),
        "types":    r'\b(int|char|float|double|long|short|unsigned|signed|void|bool|size_t|uint8_t|uint16_t|uint32_t|uint64_t|int8_t|int16_t|int32_t|int64_t)\b',
        "strings":  r'"(?:[^"\\]|\\.)*"',
        "chars":    r"'(?:[^'\\]|\\.)*'",
        "comments": r'//.*?$|/\*.*?\*/',
        "preproc":  r'^\s*#\w+',
        "numbers":  r'\b(0x[0-9a-fA-F]+|\d+\.?\d*([eE][+-]?\d+)?[fFlLuU]*)\b',
        "funcs":    r'\b([a-zA-Z_]\w*)\s*(?=\()',
        "brackets": r'[\[\]{}()]',
        "operators":r'[+\-*/%=<>!&|^~?:]',
    },
    "cpp": {
        "keywords": (
            r'\b(alignas|alignof|and|and_eq|asm|auto|bitand|bitor|bool|break|case|'
            r'catch|char|char8_t|char16_t|char32_t|class|compl|concept|const|consteval|'
            r'constexpr|constinit|const_cast|continue|co_await|co_return|co_yield|'
            r'decltype|default|delete|do|double|dynamic_cast|else|enum|explicit|export|'
            r'extern|false|float|for|friend|goto|if|inline|int|long|mutable|namespace|'
            r'new|noexcept|not|not_eq|nullptr|operator|or|or_eq|private|protected|'
            r'public|register|reinterpret_cast|requires|return|short|signed|sizeof|'
            r'static|static_assert|static_cast|struct|switch|template|this|thread_local|'
            r'throw|true|try|typedef|typeid|typename|union|unsigned|using|virtual|void|'
            r'volatile|wchar_t|while|xor|xor_eq|override|final|include|define|ifdef|'
            r'ifndef|endif|pragma|std)\b'
        ),
        "types":    r'\b(int|char|float|double|long|short|unsigned|signed|void|bool|auto|'
                    r'size_t|string|vector|map|set|list|queue|stack|pair|tuple|array|'
                    r'shared_ptr|unique_ptr|weak_ptr|optional|variant|any)\b',
        "strings":  r'"(?:[^"\\]|\\.)*"',
        "chars":    r"'(?:[^'\\]|\\.)*'",
        "comments": r'//.*?$|/\*.*?\*/',
        "preproc":  r'^\s*#\w+',
        "numbers":  r'\b(0x[0-9a-fA-F]+|\d+\.?\d*([eE][+-]?\d+)?[fFlLuU]*)\b',
        "funcs":    r'\b([a-zA-Z_]\w*)\s*(?=\()',
        "brackets": r'[\[\]{}()]',
        "operators":r'[+\-*/%=<>!&|^~?:]',
    },
    "java": {
        "keywords": (
            r'\b(abstract|assert|boolean|break|byte|case|catch|char|class|const|'
            r'continue|default|do|double|else|enum|extends|final|finally|float|for|'
            r'goto|if|implements|import|instanceof|int|interface|long|native|new|'
            r'package|private|protected|public|return|short|static|strictfp|super|'
            r'switch|synchronized|this|throw|throws|transient|try|void|volatile|while|'
            r'true|false|null|var|record|sealed|permits|yield)\b'
        ),
        "types":    r'\b(String|Integer|Double|Float|Long|Short|Byte|Boolean|Character|'
                    r'Object|Class|System|Math|StringBuilder|StringBuffer|ArrayList|'
                    r'HashMap|HashSet|LinkedList|Arrays|Collections|Optional|Stream|'
                    r'List|Map|Set|Queue|Deque|Iterator|Comparable|Iterable)\b',
        "strings":  r'"(?:[^"\\]|\\.)*"',
        "chars":    r"'(?:[^'\\]|\\.)*'",
        "comments": r'//.*?$|/\*.*?\*/',
        "preproc":  None,
        "numbers":  r'\b(\d+\.?\d*([eE][+-]?\d+)?[fFdDlL]?|0x[0-9a-fA-F]+)\b',
        "funcs":    r'\b([a-zA-Z_]\w*)\s*(?=\()',
        "brackets": r'[\[\]{}()]',
        "operators":r'[+\-*/%=<>!&|^~?:]',
        "annotations": r'@\w+',
    }
}

# ──────────────────────────────────────────────
#  SYNTAX HIGHLIGHTER
# ──────────────────────────────────────────────

class SyntaxHighlighter:
    """Applies syntax highlighting to a tkinter Text widget."""

    def __init__(self, text_widget, language="cpp"):
        self.widget = text_widget
        self.language = language
        self._job = None   # debounce handle

    def set_language(self, lang):
        self.language = lang

    def schedule(self, event=None):
        """Debounce: only run highlighting after 150 ms of inactivity."""
        if self._job:
            self.widget.after_cancel(self._job)
        self._job = self.widget.after(150, self.highlight_all)

    def highlight_all(self):
        """Clear and reapply all tags to the entire document."""
        w = self.widget
        rules = SYNTAX.get(self.language, SYNTAX["cpp"])

        # Remove existing tags
        for tag in ("kw","type","str","chr","cmt","pre","num","fn","brk","op","ann"):
            w.tag_remove(tag, "1.0", "end")

        content = w.get("1.0", "end-1c")

        def apply(tag, pattern, flags=re.MULTILINE):
            if pattern is None:
                return
            for m in re.finditer(pattern, content, flags | re.DOTALL if "cmt" in tag else flags):
                s = m.start(); e = m.end()
                start = f"1.0+{s}c"; end = f"1.0+{e}c"
                w.tag_add(tag, start, end)

        apply("cmt", rules["comments"])
        apply("pre", rules.get("preproc"))
        apply("str", rules["strings"])
        apply("chr", rules["chars"])
        apply("num", rules["numbers"])
        apply("kw",  rules["keywords"])
        apply("type",rules["types"])
        apply("fn",  rules["funcs"])
        apply("brk", rules["brackets"])
        apply("op",  rules["operators"])
        if "annotations" in rules:
            apply("ann", rules["annotations"])

    def configure_tags(self, t):
        """Bind tag colours from the active theme."""
        self.widget.tag_configure("kw",   foreground=t["purple"], font=("Cascadia Code", 11, "bold"))
        self.widget.tag_configure("type", foreground=t["teal"])
        self.widget.tag_configure("str",  foreground=t["green"])
        self.widget.tag_configure("chr",  foreground=t["green"])
        self.widget.tag_configure("cmt",  foreground=t["fg2"], font=("Cascadia Code", 11, "italic"))
        self.widget.tag_configure("pre",  foreground=t["orange"])
        self.widget.tag_configure("num",  foreground=t["orange"])
        self.widget.tag_configure("fn",   foreground=t["accent2"])
        self.widget.tag_configure("brk",  foreground=t["yellow"])
        self.widget.tag_configure("op",   foreground=t["pink"])
        self.widget.tag_configure("ann",  foreground=t["yellow"], font=("Cascadia Code", 11, "bold"))


# ──────────────────────────────────────────────
#  LINE NUMBER CANVAS
# ──────────────────────────────────────────────

class LineNumbers(tk.Canvas):
    """A canvas that mirrors line numbers alongside a Text widget."""

    def __init__(self, parent, text_widget, **kwargs):
        super().__init__(parent, **kwargs)
        self.text = text_widget
        self.bind("<ButtonPress-1>", self._on_click)

    def redraw(self, theme):
        self.delete("all")
        self.configure(bg=theme["line_bg"])
        i = self.text.index("@0,0")
        while True:
            dline = self.text.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            ln = str(i).split(".")[0]
            self.create_text(
                self.winfo_width() - 6, y,
                anchor="ne", text=ln,
                fill=theme["line_fg"],
                font=("Cascadia Code", 10)
            )
            i = self.text.index(f"{i}+1line")
            if i == self.text.index(f"{i}"):
                break

    def _on_click(self, event):
        """Select entire line when clicking on line numbers."""
        index = self.text.index(f"@0,{event.y}")
        line = index.split(".")[0]
        self.text.tag_remove("sel", "1.0", "end")
        self.text.tag_add("sel", f"{line}.0", f"{line}.end+1c")


# ──────────────────────────────────────────────
#  EDITOR TAB
# ──────────────────────────────────────────────

class EditorTab:
    """One open file: text widget + line numbers + highlighter."""

    INDENT = "    "   # 4 spaces

    def __init__(self, notebook, theme_name, theme, on_modify):
        self.filepath = None
        self.modified = False
        self.language = "cpp"
        self.theme_name = theme_name
        self.on_modify = on_modify

        # ── Outer frame for this tab ──
        self.frame = tk.Frame(notebook, bg=theme["bg"])

        # ── Horizontal pane: line numbers | editor ──
        self.pane = tk.Frame(self.frame, bg=theme["bg"])
        self.pane.pack(fill="both", expand=True)

        # Text widget
        self.text = tk.Text(
            self.pane,
            wrap="none",
            undo=True,
            font=("Cascadia Code", 11),
            bg=theme["bg"], fg=theme["fg"],
            insertbackground=theme["cursor"],
            selectbackground=theme["select_bg"],
            selectforeground=theme["fg"],
            relief="flat", bd=0,
            padx=8, pady=4,
            tabs=("1c",)
        )

        # Scrollbars
        self.vscroll = ttk.Scrollbar(self.pane, orient="vertical",   command=self._on_vscroll)
        self.hscroll = ttk.Scrollbar(self.frame, orient="horizontal", command=self.text.xview)
        self.text.configure(yscrollcommand=self.vscroll.set, xscrollcommand=self.hscroll.set)

        # Line numbers
        self.line_numbers = LineNumbers(self.pane, self.text, width=46, bg=theme["line_bg"])

        # Layout
        self.line_numbers.pack(side="left", fill="y")
        self.vscroll.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.hscroll.pack(side="bottom", fill="x")

        # Syntax highlighter
        self.highlighter = SyntaxHighlighter(self.text, self.language)
        self.highlighter.configure_tags(theme)

        # Events
        self.text.bind("<KeyRelease>",    self._on_key)
        self.text.bind("<Return>",        self._auto_indent)
        self.text.bind("<<Modified>>",    self._mark_modified)
        self.text.bind("<Configure>",     lambda e: self._redraw_ln())
        self.text.bind("<MouseWheel>",    lambda e: self._redraw_ln())
        self.text.bind("<Button-4>",      lambda e: self._redraw_ln())
        self.text.bind("<Button-5>",      lambda e: self._redraw_ln())

    # ── Scrolling ──

    def _on_vscroll(self, *args):
        self.text.yview(*args)
        self._redraw_ln()

    def _redraw_ln(self):
        self.line_numbers.redraw(THEMES[self.theme_name])

    # ── Key handler ──

    def _on_key(self, event):
        self._redraw_ln()
        self.highlighter.schedule()
        self._autocomplete_brackets(event)

    def _autocomplete_brackets(self, event):
        pairs = {"(": ")", "[": "]", "{": "}"}
        if event.char in pairs:
            close = pairs[event.char]
            pos = self.text.index("insert")
            self.text.insert(pos, close)
            self.text.mark_set("insert", pos)

    def _auto_indent(self, event):
        """On Enter, replicate the current line's leading whitespace."""
        idx = self.text.index("insert linestart")
        line = self.text.get(idx, "insert")
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]

        # Extra indent after opening brace
        if self.text.get("insert-1c") == "{":
            indent += self.INDENT

        self.text.after(1, lambda: (
            self.text.insert("insert", indent),
            self._redraw_ln()
        ))

    def _mark_modified(self, event=None):
        if self.text.edit_modified():
            self.modified = True
            self.on_modify(self)
            self.text.edit_modified(False)

    # ── Public API ──

    def apply_theme(self, theme_name, theme):
        self.theme_name = theme_name
        self.text.configure(
            bg=theme["bg"], fg=theme["fg"],
            insertbackground=theme["cursor"],
            selectbackground=theme["select_bg"]
        )
        self.frame.configure(bg=theme["bg"])
        self.pane.configure(bg=theme["bg"])
        self.line_numbers.configure(bg=theme["line_bg"])
        self.highlighter.configure_tags(theme)
        self.highlighter.highlight_all()
        self._redraw_ln()

    def detect_language(self):
        if not self.filepath:
            return
        ext = Path(self.filepath).suffix.lower()
        mapping = {".c": "c", ".cpp": "cpp", ".cc": "cpp",
                   ".cxx": "cpp", ".h": "cpp", ".hpp": "cpp", ".java": "java"}
        self.language = mapping.get(ext, "cpp")
        self.highlighter.set_language(self.language)
        self.highlighter.highlight_all()


# ──────────────────────────────────────────────
#  SEARCH/REPLACE DIALOG
# ──────────────────────────────────────────────

class SearchPanel(tk.Frame):
    """Inline search-and-replace bar at the top of the editor area."""

    def __init__(self, parent, get_text_fn, theme, **kwargs):
        super().__init__(parent, **kwargs)
        self.get_text = get_text_fn
        self._matches = []
        self._idx = -1
        self._build(theme)

    def _build(self, t):
        lbl_style = dict(bg=t["bg3"], fg=t["fg2"], font=("Segoe UI", 9))
        entry_style = dict(
            bg=t["bg2"], fg=t["fg"], insertbackground=t["cursor"],
            relief="flat", bd=0, font=("Cascadia Code", 10),
            highlightthickness=1, highlightbackground=t["border"]
        )
        btn_style = dict(bg=t["accent"], fg=t["bg"], relief="flat",
                         font=("Segoe UI", 9, "bold"), padx=6, cursor="hand2")

        self.configure(bg=t["bg3"], pady=4)

        tk.Label(self, text="Find:", **lbl_style).pack(side="left", padx=(8,2))
        self.find_var = tk.StringVar()
        self.find_entry = tk.Entry(self, textvariable=self.find_var, width=22, **entry_style)
        self.find_entry.pack(side="left", padx=2)

        tk.Label(self, text="Replace:", **lbl_style).pack(side="left", padx=(8,2))
        self.rep_var = tk.StringVar()
        tk.Entry(self, textvariable=self.rep_var, width=18, **entry_style).pack(side="left", padx=2)

        tk.Button(self, text="◀", command=self.find_prev, **btn_style).pack(side="left", padx=2)
        tk.Button(self, text="▶", command=self.find_next, **btn_style).pack(side="left", padx=2)
        tk.Button(self, text="Replace", command=self.replace_one,
                  bg=t["bg3"], fg=t["fg"], relief="flat",
                  font=("Segoe UI", 9), padx=6, cursor="hand2").pack(side="left", padx=2)
        tk.Button(self, text="All", command=self.replace_all,
                  bg=t["bg3"], fg=t["fg"], relief="flat",
                  font=("Segoe UI", 9), padx=6, cursor="hand2").pack(side="left", padx=2)

        self.count_lbl = tk.Label(self, text="", **lbl_style)
        self.count_lbl.pack(side="left", padx=8)

        tk.Button(self, text="✕", command=self.pack_forget,
                  bg=t["bg3"], fg=t["fg2"], relief="flat",
                  font=("Segoe UI", 9), cursor="hand2").pack(side="right", padx=6)

        self.find_var.trace_add("write", lambda *_: self._search())
        self.find_entry.bind("<Return>",       lambda e: self.find_next())
        self.find_entry.bind("<Shift-Return>", lambda e: self.find_prev())

    def _search(self):
        tw = self.get_text()
        if not tw:
            return
        tw.tag_remove("search_hi", "1.0", "end")
        tw.tag_remove("search_cur", "1.0", "end")
        query = self.find_var.get()
        self._matches = []
        self._idx = -1
        if not query:
            self.count_lbl.config(text="")
            return
        content = tw.get("1.0", "end-1c")
        for m in re.finditer(re.escape(query), content):
            s = f"1.0+{m.start()}c"
            e = f"1.0+{m.end()}c"
            self._matches.append((s, e))
            tw.tag_add("search_hi", s, e)
        tw.tag_configure("search_hi",  background="#f9e2af", foreground="#1e1e2e")
        tw.tag_configure("search_cur", background="#fab387", foreground="#1e1e2e")
        self.count_lbl.config(text=f"{len(self._matches)} matches")

    def _go_to(self, idx):
        tw = self.get_text()
        if not tw or not self._matches:
            return
        tw.tag_remove("search_cur", "1.0", "end")
        self._idx = idx % len(self._matches)
        s, e = self._matches[self._idx]
        tw.tag_add("search_cur", s, e)
        tw.see(s)
        self.count_lbl.config(text=f"{self._idx+1}/{len(self._matches)}")

    def find_next(self): self._go_to(self._idx + 1)
    def find_prev(self): self._go_to(self._idx - 1)

    def replace_one(self):
        tw = self.get_text()
        if not tw or self._idx < 0 or not self._matches:
            return
        s, e = self._matches[self._idx]
        tw.delete(s, e)
        tw.insert(s, self.rep_var.get())
        self._search()

    def replace_all(self):
        tw = self.get_text()
        if not tw:
            return
        q = self.find_var.get()
        r = self.rep_var.get()
        if not q:
            return
        content = tw.get("1.0", "end-1c")
        new = content.replace(q, r)
        tw.delete("1.0", "end")
        tw.insert("1.0", new)
        self._search()


# ──────────────────────────────────────────────
#  MAIN APPLICATION
# ──────────────────────────────────────────────

class PyCodeStudio(tk.Tk):
    """Main application window."""

    APP_TITLE = "PyCode Studio"
    DEFAULT_THEME = "dark"

    def __init__(self):
        super().__init__()
        self.title(self.APP_TITLE)
        self.geometry("1280x800")
        self.minsize(900, 600)

        self.theme_name = self.DEFAULT_THEME
        self._theme = THEMES[self.theme_name]
        self._tabs: list[EditorTab] = []
        self._process = None          # running subprocess
        self._run_thread = None

        self._build_ui()
        self._bind_shortcuts()
        self._new_file()              # start with one blank tab
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── UI Construction ──────────────────────────────

    def _build_ui(self):
        t = self._theme

        # ── Menu bar ──
        self._build_menu()

        # ── Toolbar ──
        self._build_toolbar()

        # ── Main paned window (editor | console) ──
        self.main_pane = tk.PanedWindow(
            self, orient="vertical",
            bg=t["bg"], sashwidth=4, sashrelief="flat",
            handlesize=0
        )
        self.main_pane.pack(fill="both", expand=True)

        # ── Editor area (notebook of tabs) ──
        self.notebook = ttk.Notebook(self.main_pane)
        self._style_notebook()
        self.main_pane.add(self.notebook, minsize=300)

        # ── Search panel (hidden by default) ──
        self.search_panel = SearchPanel(
            self, self._active_text, t,
            bg=t["bg3"]
        )
        # placed just above the notebook via pack tricks later

        # ── Bottom console area ──
        console_frame = tk.Frame(self.main_pane, bg=t["console_bg"])
        self.main_pane.add(console_frame, minsize=100)

        # Console header
        hdr = tk.Frame(console_frame, bg=t["toolbar_bg"], height=28)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text=" ⬛ OUTPUT", bg=t["toolbar_bg"], fg=t["fg2"],
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=8)
        self._lang_lbl = tk.Label(hdr, text="", bg=t["toolbar_bg"], fg=t["accent"],
                                  font=("Segoe UI", 9))
        self._lang_lbl.pack(side="left")
        tk.Button(hdr, text="🗑 Clear", bg=t["toolbar_bg"], fg=t["fg2"],
                  relief="flat", font=("Segoe UI", 9), cursor="hand2",
                  command=self._clear_console).pack(side="right", padx=8)
        tk.Button(hdr, text="⏹ Stop", bg=t["toolbar_bg"], fg=t["red"],
                  relief="flat", font=("Segoe UI", 9), cursor="hand2",
                  command=self._stop_process).pack(side="right")

        # Console text
        self.console = tk.Text(
            console_frame, height=10, wrap="word",
            bg=t["console_bg"], fg=t["console_fg"],
            insertbackground=t["cursor"],
            font=("Cascadia Code", 10),
            relief="flat", state="disabled", padx=8, pady=4
        )
        cscroll = ttk.Scrollbar(console_frame, command=self.console.yview)
        self.console.configure(yscrollcommand=cscroll.set)
        cscroll.pack(side="right", fill="y")
        self.console.pack(fill="both", expand=True)

        # Console tags
        self.console.tag_configure("err",  foreground=t["error_fg"])
        self.console.tag_configure("info", foreground=t["accent"])
        self.console.tag_configure("ok",   foreground=t["green"])
        self.console.tag_configure("time", foreground=t["fg2"])

        # ── Status bar ──
        self.status = tk.Frame(self, bg=t["toolbar_bg"], height=22)
        self.status.pack(fill="x", side="bottom")
        self.status.pack_propagate(False)
        self._status_lbl = tk.Label(self.status, text="Ready", bg=t["toolbar_bg"],
                                    fg=t["fg2"], font=("Segoe UI", 9), anchor="w")
        self._status_lbl.pack(side="left", padx=8)
        self._pos_lbl = tk.Label(self.status, text="Ln 1, Col 1",
                                 bg=t["toolbar_bg"], fg=t["fg2"], font=("Segoe UI", 9))
        self._pos_lbl.pack(side="right", padx=8)
        self.bind_all("<ButtonRelease-1>", self._update_pos)
        self.bind_all("<KeyRelease>",      self._update_pos)

    def _build_menu(self):
        t = self._theme
        self._menubar = tk.Menu(self, bg=t["bg2"], fg=t["fg"],
                                activebackground=t["accent"],
                                activeforeground=t["bg"],
                                relief="flat", bd=0)
        self.configure(menu=self._menubar)

        def menu(label, items):
            m = tk.Menu(self._menubar, tearoff=0,
                        bg=t["bg2"], fg=t["fg"],
                        activebackground=t["accent"], activeforeground=t["bg"],
                        relief="flat", bd=0)
            self._menubar.add_cascade(label=label, menu=m)
            for item in items:
                if item[0] == "---":
                    m.add_separator()
                elif len(item) >= 2:
                    lbl = item[0]
                    cmd = item[1]
                    acc = item[2] if len(item) > 2 else ""
                    m.add_command(label=lbl, command=cmd, accelerator=acc)
            return m

        menu("File", [
            ("New",     self._new_file,   "Ctrl+N"),
            ("Open…",   self._open_file,  "Ctrl+O"),
            ("---",),
            ("Save",    self._save_file,  "Ctrl+S"),
            ("Save As…",self._save_as,    "Ctrl+Shift+S"),
            ("---",),
            ("Close Tab",self._close_tab, "Ctrl+W"),
            ("Exit",    self._on_close,   "Alt+F4"),
        ])
        menu("Edit", [
            ("Undo",    lambda: self._active_tab() and self._active_tab().text.edit_undo(), "Ctrl+Z"),
            ("Redo",    lambda: self._active_tab() and self._active_tab().text.edit_redo(), "Ctrl+Y"),
            ("---",),
            ("Cut",     lambda: self.focus_get() and self.focus_get().event_generate("<<Cut>>"),   "Ctrl+X"),
            ("Copy",    lambda: self.focus_get() and self.focus_get().event_generate("<<Copy>>"),  "Ctrl+C"),
            ("Paste",   lambda: self.focus_get() and self.focus_get().event_generate("<<Paste>>"), "Ctrl+V"),
            ("---",),
            ("Select All", self._select_all, "Ctrl+A"),
            ("---",),
            ("Find / Replace", self._show_search, "Ctrl+F"),
        ])
        menu("View", [
            ("Toggle Theme", self._toggle_theme, "Ctrl+T"),
            ("Increase Font", lambda: self._change_font(+1), "Ctrl++"),
            ("Decrease Font", lambda: self._change_font(-1), "Ctrl+-"),
        ])
        menu("Run", [
            ("Run / Compile", self._run_code, "F5"),
            ("Stop",          self._stop_process, ""),
        ])
        menu("Help", [
            ("About", self._about),
        ])

    def _build_toolbar(self):
        t = self._theme
        tb = tk.Frame(self, bg=t["toolbar_bg"], height=38)
        tb.pack(fill="x")
        tb.pack_propagate(False)

        def tbtn(icon, tip, cmd, color=None):
            b = tk.Button(
                tb, text=icon, command=cmd,
                bg=t["toolbar_bg"], fg=color or t["fg"],
                relief="flat", font=("Segoe UI", 13),
                padx=6, pady=2, cursor="hand2",
                activebackground=t["bg3"], activeforeground=t["fg"]
            )
            b.pack(side="left", padx=1)
            self._add_tooltip(b, tip)
            return b

        tbtn("📄", "New (Ctrl+N)",         self._new_file)
        tbtn("📂", "Open (Ctrl+O)",        self._open_file)
        tbtn("💾", "Save (Ctrl+S)",        self._save_file)
        tk.Frame(tb, bg=t["border"], width=1).pack(side="left", fill="y", padx=4)
        tbtn("↩", "Undo (Ctrl+Z)",         lambda: self._active_tab() and self._active_tab().text.edit_undo())
        tbtn("↪", "Redo (Ctrl+Y)",         lambda: self._active_tab() and self._active_tab().text.edit_redo())
        tk.Frame(tb, bg=t["border"], width=1).pack(side="left", fill="y", padx=4)
        tbtn("🔍", "Find (Ctrl+F)",        self._show_search)
        tk.Frame(tb, bg=t["border"], width=1).pack(side="left", fill="y", padx=4)
        self._run_btn = tbtn("▶  Run", "Run / Compile (F5)", self._run_code, t["green"])
        tk.Frame(tb, bg=t["border"], width=1).pack(side="left", fill="y", padx=4)
        tbtn("🌙", "Toggle Theme (Ctrl+T)", self._toggle_theme)

        # Language selector
        tk.Label(tb, text=" Language:", bg=t["toolbar_bg"], fg=t["fg2"],
                 font=("Segoe UI", 9)).pack(side="right", padx=(0,4))
        self._lang_var = tk.StringVar(value="C++")
        lang_menu = ttk.Combobox(tb, textvariable=self._lang_var,
                                 values=["C", "C++", "Java"],
                                 state="readonly", width=7,
                                 font=("Segoe UI", 9))
        lang_menu.pack(side="right", padx=(0, 8))
        lang_menu.bind("<<ComboboxSelected>>", self._on_lang_change)

    def _style_notebook(self):
        style = ttk.Style()
        style.theme_use("default")
        t = self._theme
        style.configure("TNotebook",
                        background=t["toolbar_bg"], borderwidth=0, tabmargins=0)
        style.configure("TNotebook.Tab",
                        background=t["tab_inactive"], foreground=t["fg2"],
                        padding=[10, 4], font=("Segoe UI", 9),
                        borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", t["tab_active"])],
                  foreground=[("selected", t["fg"])])
        style.configure("Vertical.TScrollbar",
                        background=t["bg3"], troughcolor=t["bg2"],
                        arrowcolor=t["fg2"], borderwidth=0)
        style.configure("Horizontal.TScrollbar",
                        background=t["bg3"], troughcolor=t["bg2"],
                        arrowcolor=t["fg2"], borderwidth=0)
        style.configure("TCombobox",
                        fieldbackground=t["bg3"], background=t["bg3"],
                        foreground=t["fg"], selectbackground=t["select_bg"],
                        arrowcolor=t["fg2"])

    # ── Tab management ─────────────────────────────

    def _new_file(self):
        tab = EditorTab(self.notebook, self.theme_name, self._theme, self._tab_modified)
        self._tabs.append(tab)
        self.notebook.add(tab.frame, text=" Untitled ")
        self.notebook.select(tab.frame)
        tab.text.focus_set()
        self._sync_lang_selector(tab)
        self._set_status("New file created")

    def _active_tab(self) -> EditorTab | None:
        try:
            idx = self.notebook.index(self.notebook.select())
            return self._tabs[idx]
        except Exception:
            return None

    def _active_text(self) -> tk.Text | None:
        tab = self._active_tab()
        return tab.text if tab else None

    def _tab_modified(self, tab: EditorTab):
        idx = self._tabs.index(tab)
        title = self._tab_title(tab)
        self.notebook.tab(idx, text=f" {title}* ")

    def _tab_title(self, tab: EditorTab):
        if tab.filepath:
            return Path(tab.filepath).name
        return "Untitled"

    def _close_tab(self):
        tab = self._active_tab()
        if not tab:
            return
        if tab.modified:
            r = messagebox.askyesnocancel("Unsaved changes",
                f"{self._tab_title(tab)} has unsaved changes. Save before closing?")
            if r is None:
                return
            if r:
                self._save_file()
        idx = self._tabs.index(tab)
        self._tabs.pop(idx)
        self.notebook.forget(idx)
        if not self._tabs:
            self._new_file()

    # ── File operations ────────────────────────────

    def _open_file(self, path=None):
        if not path:
            path = filedialog.askopenfilename(
                filetypes=[
                    ("C files", "*.c"),
                    ("C++ files", "*.cpp *.cc *.cxx *.h *.hpp"),
                    ("Java files", "*.java"),
                    ("All files", "*.*"),
                ]
            )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open file:\n{e}")
            return

        # Reuse blank untitled tab if empty
        tab = self._active_tab()
        if tab and not tab.filepath and not tab.modified and not tab.text.get("1.0", "end-1c").strip():
            pass
        else:
            self._new_file()
            tab = self._active_tab()

        tab.filepath = path
        tab.text.delete("1.0", "end")
        tab.text.insert("1.0", content)
        tab.text.edit_modified(False)
        tab.modified = False
        tab.detect_language()

        idx = self._tabs.index(tab)
        self.notebook.tab(idx, text=f" {Path(path).name} ")
        self._sync_lang_selector(tab)
        tab.highlighter.highlight_all()
        tab.line_numbers.redraw(self._theme)
        self._set_status(f"Opened: {path}")

    def _save_file(self):
        tab = self._active_tab()
        if not tab:
            return
        if not tab.filepath:
            self._save_as()
            return
        self._write_file(tab, tab.filepath)

    def _save_as(self):
        tab = self._active_tab()
        if not tab:
            return
        lang_map = {"c": [("C files","*.c")], "cpp": [("C++ files","*.cpp")],
                    "java": [("Java files","*.java")]}
        ft = lang_map.get(tab.language, []) + [("All files","*.*")]
        path = filedialog.asksaveasfilename(filetypes=ft, defaultextension=".cpp")
        if not path:
            return
        self._write_file(tab, path)
        tab.filepath = path
        tab.detect_language()
        idx = self._tabs.index(tab)
        self.notebook.tab(idx, text=f" {Path(path).name} ")
        self._sync_lang_selector(tab)

    def _write_file(self, tab, path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(tab.text.get("1.0", "end-1c"))
            tab.modified = False
            idx = self._tabs.index(tab)
            self.notebook.tab(idx, text=f" {Path(path).name} ")
            self._set_status(f"Saved: {path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    # ── Language ───────────────────────────────────

    def _on_lang_change(self, event=None):
        tab = self._active_tab()
        if not tab:
            return
        name_map = {"C": "c", "C++": "cpp", "Java": "java"}
        tab.language = name_map.get(self._lang_var.get(), "cpp")
        tab.highlighter.set_language(tab.language)
        tab.highlighter.highlight_all()

    def _sync_lang_selector(self, tab: EditorTab):
        rev = {"c": "C", "cpp": "C++", "java": "Java"}
        self._lang_var.set(rev.get(tab.language, "C++"))
        self._lang_lbl.config(text=f"  [{rev.get(tab.language,'')}]")

    # ── Run / Compile ──────────────────────────────

    def _run_code(self):
        tab = self._active_tab()
        if not tab:
            return
        if tab.modified or not tab.filepath:
            self._save_file()
            if not tab.filepath:
                self._console_write("⚠  Please save the file first.\n", "err")
                return

        self._clear_console()
        lang = tab.language
        fp   = tab.filepath
        fdir = str(Path(fp).parent)
        fname = Path(fp).stem

        if lang == "c":
            out = str(Path(fdir) / fname)
            cmds = [[" gcc", fp, "-o", out, "-lm"], [out]]
        elif lang == "cpp":
            out = str(Path(fdir) / fname)
            cmds = [["g++", fp, "-o", out, "-std=c++17"], [out]]
        elif lang == "java":
            cmds = [["javac", fp], ["java", "-cp", fdir, fname]]
        else:
            self._console_write("Unknown language.\n", "err")
            return

        self._console_write(f"⚙  Building {Path(fp).name} …\n", "info")
        self._run_btn.config(state="disabled")
        self._run_thread = threading.Thread(target=self._exec_pipeline,
                                            args=(cmds,), daemon=True)
        self._run_thread.start()

    def _exec_pipeline(self, cmds):
        t0 = time.time()
        for cmd in cmds:
            self._console_write(f"$ {' '.join(cmd)}\n", "time")
            try:
                self._process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                out, err = self._process.communicate(timeout=30)
                rc = self._process.returncode
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._console_write("⚠  Process timed out (30s).\n", "err")
                break
            except FileNotFoundError as e:
                self._console_write(f"⚠  {e}\n   Is the compiler installed?\n", "err")
                break
            except Exception as e:
                self._console_write(f"⚠  {e}\n", "err")
                break

            if out:
                self._console_write(out)
            if err:
                tag = "err" if rc != 0 else "time"
                self._console_write(err, tag)
            if rc != 0:
                self._console_write(f"\n✗  Exited with code {rc}\n", "err")
                break
        else:
            elapsed = time.time() - t0
            self._console_write(f"\n✓  Done in {elapsed:.2f}s\n", "ok")

        self.after(0, lambda: self._run_btn.config(state="normal"))

    def _stop_process(self):
        if self._process and self._process.poll() is None:
            self._process.terminate()
            self._console_write("\n⏹  Process stopped.\n", "err")

    def _console_write(self, text, tag=None):
        def _do():
            self.console.config(state="normal")
            if tag:
                self.console.insert("end", text, tag)
            else:
                self.console.insert("end", text)
            self.console.see("end")
            self.console.config(state="disabled")
        self.after(0, _do)

    def _clear_console(self):
        self.console.config(state="normal")
        self.console.delete("1.0", "end")
        self.console.config(state="disabled")

    # ── Search ─────────────────────────────────────

    def _show_search(self):
        t = self._theme
        self.search_panel.configure(bg=t["bg3"])
        # Pack above the paned window
        if not self.search_panel.winfo_ismapped():
            self.search_panel.pack(fill="x", before=self.main_pane)
        self.search_panel.find_entry.focus_set()

    # ── Theme ──────────────────────────────────────

    def _toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self._theme = THEMES[self.theme_name]
        self._apply_theme()

    def _apply_theme(self):
        t = self._theme
        self.configure(bg=t["bg"])
        for tab in self._tabs:
            tab.apply_theme(self.theme_name, t)
        self._style_notebook()
        self.console.configure(bg=t["console_bg"], fg=t["console_fg"])
        self.console.tag_configure("err",  foreground=t["error_fg"])
        self.console.tag_configure("info", foreground=t["accent"])
        self.console.tag_configure("ok",   foreground=t["green"])
        self.console.tag_configure("time", foreground=t["fg2"])
        self.status.configure(bg=t["toolbar_bg"])
        self._status_lbl.configure(bg=t["toolbar_bg"], fg=t["fg2"])
        self._pos_lbl.configure(bg=t["toolbar_bg"], fg=t["fg2"])

    # ── Font size ──────────────────────────────────

    def _change_font(self, delta):
        for tab in self._tabs:
            cur = tab.text.cget("font")
            try:
                f = font.Font(font=cur)
                size = max(8, f.actual()["size"] + delta)
                tab.text.configure(font=("Cascadia Code", size))
                tab.line_numbers.redraw(self._theme)
            except Exception:
                pass

    # ── Keyboard shortcuts ─────────────────────────

    def _bind_shortcuts(self):
        self.bind("<Control-n>", lambda e: self._new_file())
        self.bind("<Control-o>", lambda e: self._open_file())
        self.bind("<Control-s>", lambda e: self._save_file())
        self.bind("<Control-S>", lambda e: self._save_as())
        self.bind("<Control-w>", lambda e: self._close_tab())
        self.bind("<Control-f>", lambda e: self._show_search())
        self.bind("<Control-t>", lambda e: self._toggle_theme())
        self.bind("<F5>",        lambda e: self._run_code())
        self.bind("<Control-equal>", lambda e: self._change_font(+1))
        self.bind("<Control-minus>", lambda e: self._change_font(-1))
        self.bind("<Control-a>",     lambda e: self._select_all())

    def _select_all(self):
        tab = self._active_tab()
        if tab:
            tab.text.tag_add("sel", "1.0", "end")

    # ── Status bar update ──────────────────────────

    def _update_pos(self, event=None):
        tab = self._active_tab()
        if not tab:
            return
        try:
            pos = tab.text.index("insert")
            ln, col = pos.split(".")
            self._pos_lbl.config(text=f"Ln {ln}, Col {int(col)+1}")
        except Exception:
            pass

    def _set_status(self, msg):
        self._status_lbl.config(text=msg)
        self.after(4000, lambda: self._status_lbl.config(text="Ready"))

    # ── Tooltip helper ─────────────────────────────

    def _add_tooltip(self, widget, text):
        tip = None
        def show(e):
            nonlocal tip
            x = widget.winfo_rootx() + 10
            y = widget.winfo_rooty() + widget.winfo_height() + 4
            tip = tk.Toplevel(self)
            tip.wm_overrideredirect(True)
            tip.wm_geometry(f"+{x}+{y}")
            tk.Label(tip, text=text, bg="#2a2a3a", fg="#cdd6f4",
                     font=("Segoe UI", 8), relief="flat", padx=6, pady=3).pack()
        def hide(e):
            nonlocal tip
            if tip:
                tip.destroy()
                tip = None
        widget.bind("<Enter>", show)
        widget.bind("<Leave>", hide)

    # ── Misc ───────────────────────────────────────

    def _about(self):
        messagebox.showinfo("About PyCode Studio",
            "PyCode Studio\n"
            "A lightweight VS Code-like editor for C, C++, Java\n\n"
            "Built with Python + tkinter\n\n"
            "Keyboard shortcuts:\n"
            "  Ctrl+N   New file\n"
            "  Ctrl+O   Open file\n"
            "  Ctrl+S   Save\n"
            "  Ctrl+W   Close tab\n"
            "  Ctrl+F   Find / Replace\n"
            "  F5       Run / Compile\n"
            "  Ctrl+T   Toggle theme\n"
            "  Ctrl++/- Font size\n"
        )

    def _on_close(self):
        for tab in self._tabs:
            if tab.modified:
                r = messagebox.askyesnocancel("Unsaved changes",
                    f"{self._tab_title(tab)} has unsaved changes. Save?")
                if r is None:
                    return
                if r:
                    self._tabs[self._tabs.index(tab)]
                    self.notebook.select(self._tabs.index(tab))
                    self._save_file()
        self.destroy()


# ──────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────

if __name__ == "__main__":
    app = PyCodeStudio()
    app.mainloop()
