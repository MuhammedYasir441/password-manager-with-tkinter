import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import string
import json
import os

# File name for storing passwords
PASSWORDS_FILE = 'passwords.json'

def load_passwords():
    """Loads passwords from the JSON file"""
    if os.path.exists(PASSWORDS_FILE):
        try:
            with open(PASSWORDS_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "The JSON file contains an invalid format.")
            return {}
        except Exception as e:
            messagebox.showerror("Error", f"File read error: {e}")
            return {}
    return {}

def save_passwords():
    """Saves passwords to the JSON file"""
    try:
        with open(PASSWORDS_FILE, 'w') as file:
            json.dump(passwords, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"File write error: {e}")

def generate_password(length, use_uppercase, use_lowercase, use_digits, use_special):
    """Generates a password based on specified criteria"""
    characters = ""
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if not characters:
        messagebox.showerror("Error", "At least one type of character must be selected.")
        return ""
    
    return ''.join(random.choice(characters) for _ in range(length))

def save_password():
    """Creates and saves a new password"""
    name = simpledialog.askstring("New Password", "Enter a name for the password:")
    if not name:
        return

    if name in passwords:
        messagebox.showerror("Error", "This name already exists.")
        return
    
    try:
        length = int(simpledialog.askstring("New Password", "Enter password length:"))
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid length.")
        return
    
    use_uppercase = messagebox.askyesno("New Password", "Include uppercase letters?")
    use_lowercase = messagebox.askyesno("New Password", "Include lowercase letters?")
    use_digits = messagebox.askyesno("New Password", "Include digits?")
    use_special = messagebox.askyesno("New Password", "Include special characters?")
    
    password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_special)
    if password:
        passwords[name] = password
        save_passwords()
        refresh_password_list()

def copy_password(password):
    """Copies the password to the clipboard"""
    root.clipboard_clear()
    root.clipboard_append(password)
    messagebox.showinfo("Info", "Password copied to clipboard.")

def edit_password(name):
    """Edits an existing password"""
    new_password = simpledialog.askstring("Edit Password", f"Enter a new password for {name}:", initialvalue=passwords.get(name, ""))
    if new_password is not None:
        passwords[name] = new_password
        save_passwords()
        refresh_password_list()

def delete_password(name):
    """Deletes a password"""
    if messagebox.askyesno("Delete", f"Are you sure you want to delete the password for {name}?"):
        del passwords[name]
        save_passwords()
        refresh_password_list()

def refresh_password_list():
    """Refreshes the list of passwords displayed"""
    for widget in password_list_frame.winfo_children():
        widget.destroy()
    
    for name, password in passwords.items():
        frame = tk.Frame(password_list_frame, bg='#f0f0f0', padx=10, pady=5)
        frame.pack(fill=tk.X, pady=2, padx=10)

        name_label = tk.Label(frame, text=name, font=('Arial', 12), bg='#f0f0f0')
        name_label.pack(side=tk.LEFT, padx=10)

        edit_button = tk.Button(frame, text="Edit", command=lambda n=name: edit_password(n), bg='#4CAF50', fg='white', relief='raised')
        edit_button.pack(side=tk.LEFT, padx=5)

        copy_button = tk.Button(frame, text="Copy", command=lambda p=password: copy_password(p), bg='#2196F3', fg='white', relief='raised')
        copy_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(frame, text="Delete", command=lambda n=name: delete_password(n), bg='#F44336', fg='white', relief='raised')
        delete_button.pack(side=tk.LEFT, padx=5)

def open_main_window():
    """Creates and opens the main window"""
    global root, password_list_frame

    root = tk.Tk()
    root.title("Password Manager")
    root.geometry("600x400")  # Set the window size
    root.configure(bg='#e0e0e0')

    # Add title label
    title_label = tk.Label(root, text="Password Manager", font=('Arial', 18, 'bold'), bg='#e0e0e0', pady=10)
    title_label.pack()

    # Password list frame
    password_list_frame = tk.Frame(root, bg='#e0e0e0')
    password_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    refresh_password_list()

    # New password button
    new_password_button = tk.Button(root, text="+ New Password", command=save_password, bg='#FF5722', fg='white', font=('Arial', 12), relief='raised')
    new_password_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    passwords = load_passwords()  # Load passwords
    open_main_window()
