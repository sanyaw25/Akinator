import tkinter as tk
from ui.theme import *
from engine.logic import AkinatorEngine

from data.animals import ANIMALS
from data.anime import ANIME
from data.countries import COUNTRIES
from data.food import FOOD
from data.game_characters import GAME_CHARACTERS
from data.genshin import GENSHIN
from data.movies import MOVIES
from data.objects import OBJECTS
from data.pokemon import POKEMON
from data.superheroes import SUPERHEROES

CATEGORIES = {
    "🐾 Animals": ANIMALS,
    "🎌 Cartoon": ANIME,
    "🌍 Countries": COUNTRIES,
    "🍔 Khana": FOOD,
    "🎮 Characters": GAME_CHARACTERS,
    "🌟 Genshin": GENSHIN,
    "🎬 Films": MOVIES,
    "📦 Objects": OBJECTS,
    "⚡ Cartoon 2.0": POKEMON,
    "🦸 Superheroes": SUPERHEROES,
}


class App:
    def __init__(self, root):
        self.root = root
        root.title("💖 Cute Akinator")
        root.geometry("560x500")
        root.configure(bg=BG)

        # Title
        tk.Label(
            root,
            text="💖 Cute Akinator",
            bg=BG, fg=TXT,
            font=TITLE_FONT
        ).pack(pady=10)

        # Subtitle
        tk.Label(
            root,
            text="Think of something — I adapt my questions as we go ✨",
            bg=BG, fg=TXT,
            font=("Helvetica", 11, "italic")
        ).pack()

        # Main text
        self.text = tk.Label(
            root,
            text="",
            wraplength=500,
            justify="center",
            bg=BG, fg=TXT,
            font=TEXT_FONT
        )
        self.text.pack(pady=25)
        self.buttons = tk.Frame(root, bg=BG)
        self.buttons.pack()

        self.engine = None
        self.current_data = None

        self.menu()

    def menu(self):
        self.clear_buttons()
        self.text.config(text="Choose a category 💭")

        for name, data in CATEGORIES.items():
            self.add_button(name, lambda d=data: self.start_category(d))

    def start_category(self, data):
        self.current_data = data
        self.engine = AkinatorEngine(data, self.update_ui)
        self.engine.start()

    def update_ui(self, text, finished, confidence=0):
        self.clear_buttons()
        self.text.config(text=text)

        if finished:
            self.add_button("👍 Yes, correct!", self.menu)

            if confidence < 85:
                self.add_button("🔍 Continue guessing", self.continue_guessing)

            self.add_button("🔄 Restart category", self.restart_category)
            self.add_button("🏠 Change category", self.menu)

        else:
            self.add_button("👍 Yes", lambda: self.engine.answer(True))
            self.add_button("👎 No", lambda: self.engine.answer(False))

    def continue_guessing(self):
        self.engine.ask_next()

    def restart_category(self):
        self.engine.reset()
        self.engine.start()

    def add_button(self, text, command):
        tk.Button(
            self.buttons,
            text=text,
            command=command,
            font=BTN_FONT,
            bg=BTN,
            relief="flat",
            padx=20,
            pady=10,
            width=30,
            activebackground="#ff8fab"
        ).pack(pady=6)

    def clear_buttons(self):
        for w in self.buttons.winfo_children():
            w.destroy()


root = tk.Tk()
App(root)
root.mainloop()
