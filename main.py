from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


# methods
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_input.delete(0, END)
    random_letters = [choice(letters) for _ in range(randint(8, 10))]
    random_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    random_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_list = random_letters + random_numbers + random_symbols
    shuffle(password_list)
    password = "".join(password_list)
    pyperclip.copy(password)
    password_input.insert(0, password)


def check_valid_inputs(website, email, password):
    return len(website) > 0 and len(email) > 0 and len(password) > 0


def search_website():
    website = website_input.get()

    if len(website) == 0:
        messagebox.showerror(title="Oops", message="You need to fill out a website to search for it")
        return

    try:
        with open("passwords.json", "r") as passwords_file:
            password_data = json.load(passwords_file)  # read previous data
    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="You have not added any passwords yet. Try adding a password.")
    else:
        if website in password_data:
            website_data = password_data[website]
            messagebox.showinfo(title="Your password data", message=f"Email: {website_data['email']} \n Password: {website_data['password']}")
        else:
            messagebox.showinfo(title="Oops", message="No password exists for this website")
    finally:
        website_input.delete(0, END)


def add_website_to_json(password_data, website):
    with open("passwords.json", "w") as passwords_file:
        json.dump(password_data, passwords_file, indent=4)  # save updated data

    messagebox.showinfo(title="Success!", message=f"Password was saved for {website}!")


def save_password():
    website = website_input.get()
    email = email_username_input.get()
    password = password_input.get()
    new_password_data = {
        website: {
            "email" : email,
            "password": password
        }
    }

    # if any field is not filled
    if not check_valid_inputs(website, email, password):
        messagebox.showerror(title="Oops", message="Please fill in those empty fields")
        return

    try:
        with open("passwords.json", "r") as passwords_file:
            password_data = json.load(passwords_file)  # read previous data
    except FileNotFoundError:
        add_website_to_json(new_password_data, website)
    else:
        password_data.update(new_password_data)  # update data
        add_website_to_json(password_data, website)
    finally:
        website_input.delete(0, END)
        password_input.delete(0, END)


# canvas
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(130, 100, image=logo_img)
canvas.grid(column=1, row=0)

# labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# inputs
website_input = Entry(width=21)
website_input.grid(column=1, row=1, sticky="EW")
website_input.focus()

email_username_input = Entry(width=35)
email_username_input.grid(column=1, row=2, columnspan=2, sticky="EW")
email_username_input.insert(0, "mel@test.com")

password_input = Entry(width=21)
password_input.grid(column=1, row=3, sticky="EW")

# buttons
search_button = Button(text="Search", command=search_website)
search_button.grid(column=2, row=1, sticky="EW")

password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3, sticky="EW")

add_button = Button(text="Add", width=36, command=save_password)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

window.mainloop()
