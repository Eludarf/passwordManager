from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT = ("Courier", 12, "bold")
BUTTON_FONT = ("Courier", 10, "bold")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    w = website_entry.get().strip()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="There is no data to read from.")
    else:
        key_name = list(data.keys())
        if w == key_name[0]:
            messagebox.showinfo(title="SiteLogin", message=f"Email/Username: {data[key_name[0]]["email"]}\n"
                                                           f"Password: {data[key_name[0]]["password"]}")
        else:
            messagebox.showinfo(title="SiteLogin", message=f"There is no data for '{w}' website")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def get_info():

    w = website_entry.get().strip()
    e = email_or_username_entry.get()
    p = password_entry.get()
    new_data = {
        w: {
            "email": e,
            "password": p,
        }
    }

    if w == "" or p == "":
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=w, message=f"These are the details entered: \nEmail: {e}"
                                                        f"\nPassword: {p} \nIs it ok to save?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                website_entry.focus()

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels

website_label = Label()
website_label.config(text="Website:", font=FONT)
website_label.grid(column=0, row=1)

email_or_username_label = Label()
email_or_username_label.config(text="Email/Username:", font=FONT)
email_or_username_label.grid(column=0, row=2)

password_label = Label()
password_label.config(text="Password:", font=FONT)
password_label.grid(column=0, row=3)

# -------------------------------------
# Method for stretching column:
# r = Label(bg="red", width=20, height=5)
# r.grid(row=0, column=0, columnspan=2)
# -------------------------------------

# Buttons

generate_password_button = Button()
generate_password_button.config(text="Generate Password", font=BUTTON_FONT, command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = Button()
add_button.config(text="Add", font=BUTTON_FONT, width=43, command=get_info)
add_button.grid(column=1, row=5, columnspan=2)

search_button = Button()
search_button.config(text="Search", font=BUTTON_FONT, command=find_password, width=17)
search_button.grid(column=2, row=1)

# Entry

website_entry = Entry()
website_entry.config(width=25)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_or_username_entry = Entry()
email_or_username_entry.config(width=50)
email_or_username_entry.grid(column=1, row=2, columnspan=2)
email_or_username_entry.insert(0, "random@gmail.com")

password_entry = Entry()
password_entry.config(width=25)
password_entry.grid(column=1, row=3)


window.mainloop()
