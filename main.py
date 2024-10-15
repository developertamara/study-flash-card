from tkinter import *

import pandas
from pandas import *
from tkinter import messagebox
import random

BACKGROUND_COLOR = "#B1DDC6"
current_fr_word = ""
en_value = ""
unknown_words = {}
# Read data from CSV file.
try:
    with open("data/words_to_learn.csv") as file:
        data = read_csv(file)
        french_dict = data.set_index(data.columns[0])[data.columns[1]].to_dict()
except FileNotFoundError:
    with open("data/french_words.csv") as file:
        original_data = read_csv(file)
        french_dict = original_data.set_index(original_data.columns[0])[original_data.columns[1]].to_dict()


def generate_fr_words():
    global current_fr_word
    global en_value
    global flip_timer
    window.after_cancel(flip_timer)
    current_fr_word, en_value = random.choice(list(french_dict.items()))
    canvas.itemconfig(word_text, text=current_fr_word, fill="black")
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(canvas_image, image=front_image)
    flip_timer = window.after(3000, func=flip_card)
    unknown_words[current_fr_word] = en_value
    # print(unknown_words)

def back_to_french():
    canvas.itemconfig(word_text, text=current_fr_word, fill="black")
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(canvas_image, image=front_image)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(canvas_image, image=flipped_image)
    canvas.itemconfig(word_text, text=en_value, fill="white")
    canvas.itemconfig(title_text, text="English", fill="white")

def known_words():
    french_dict.pop(current_fr_word)
    print(len(french_dict))
    known = pandas.DataFrame(list(french_dict.items()), columns=['French', 'English'])
    known.to_csv("data/words_to_learn.csv", index=False)
    generate_fr_words()

# Creating UI
window = Tk()
window.title("Billie's French Flashcards")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
front_image = PhotoImage(file="Images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=front_image)
flipped_image = PhotoImage(file="Images/card_back.png")
title_text = canvas.create_text(400, 150, text="title", fill="black", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="word", fill="black", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=3)

right_image = PhotoImage(file="Images/right.png")
right_button = Button(image=right_image, highlightthickness=0, padx=50, pady=50, command=known_words)
right_button.grid(column=0, row=1)

wrong_image = PhotoImage(file="Images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, padx=50, pady=50, command=generate_fr_words)
wrong_button.grid(column=1, row=1)

back_image = PhotoImage(file="Images/back_icon.png")
back_button = Button(image=back_image, highlightthickness=0, padx=50, pady=50, command=back_to_french)
back_button.grid(column=2, row=1)

generate_fr_words()

window.mainloop()