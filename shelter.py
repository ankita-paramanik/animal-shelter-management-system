mport mysql.connector as ms
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Connect to MySQL database
def connect_database():
    try:
        mycon = ms.connect(
            host='localhost',
            database='Animal_Shelter',
            user='root',
            password='sql4gauri'
        )
        return mycon
    except ms.Error as err:
        messagebox.showerror("Database Connection Error", str(err))
        return None

# Function for the home page
def homepage(notebook):
    frame = tk.Frame(notebook)
    notebook.add(frame, text="Home Page")

    frame.configure(bg='light blue')
    try:
        hp = tk.PhotoImage(file='Homepage.png')  # Ensure the image path is correct
        hp_disp = tk.Label(frame, image=hp)
        hp_disp.image = hp  # Keep a reference to avoid garbage collection
        hp_disp.pack(fill=tk.Y, expand=True)
    except Exception as e:
        messagebox.showerror("Image Error", f"Error loading image: {e}")

# Function for displaying shelter data
def shelter_data(notebook):
    frame = tk.Frame(notebook)
    notebook.add(frame, text="Shelter Data")

    columns = ('ID', 'Metric', 'Value')
    tree = ttk.Treeview(frame, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    t_animals = tk.Button(frame, text="Animals", command=lambda: Animals_disp(tree))
    t_adoptions = tk.Button(frame, text="Adoptions", command=lambda: Adoptions_disp(tree))
    finance = tk.Button(frame, text="Finance", command=lambda: Finance_disp(tree))

    t_animals.pack(pady=5)
    t_adoptions.pack(pady=5)
    finance.pack(pady=5)

def Animals_disp(tree):
    try:
        mycon = connect_database()
        if mycon is None:
            return
        cursor = mycon.cursor()
        cursor.execute("SELECT * FROM Operations")
        results = cursor.fetchall()
        tree.delete(*tree.get_children())  # Clear the treeview
        for row in results:
            tree.insert("", tk.END, values=row)
    except ms.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if mycon:
            cursor.close()
            mycon.close()

def Adoptions_disp(tree):
    try:
        mycon = connect_database()
        if mycon is None:
            return
        cursor = mycon.cursor()
        cursor.execute("SELECT * FROM Adoption")
        results = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in results:
            tree.insert("", tk.END, values=row)
    except ms.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if mycon:
            cursor.close()
            mycon.close()

def Finance_disp(tree):
    try:
        mycon = connect_database()
        if mycon is None:
            return
        cursor = mycon.cursor()
        cursor.execute("SELECT * FROM Finance")
        results = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in results:
            tree.insert("", tk.END, values=row)
    except ms.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if mycon:
            cursor.close()
            mycon.close()

# Registration and login functions
def register_user(username, password, notebook):
    try:
        mycon = connect_database()
        if mycon is None:
            return
        cursor = mycon.cursor()
        cursor.execute("SELECT * FROM Users WHERE Username = %s", (username,))
        result = cursor.fetchone()
        if result:
            messagebox.showwarning("Warning", "Username already exists!")
        else:
            cursor.execute("INSERT INTO Users (Username, Password) VALUES (%s, %s)", (username, password))
            mycon.commit()
            messagebox.showinfo("Success", "Registration successful!")
            add_animal(notebook, username)
            load_adoption_page(notebook, username, None)
    except ms.Error as err:
        messagebox.showerror("Database Error", f"Error during registration: {str(err)}")
    finally:
        if mycon:
            cursor.close()
            mycon.close()

def login_user(username, password, notebook):
    try:
        mycon = connect_database()
        if mycon is None:
            return
        cursor = mycon.cursor()
        cursor.execute("SELECT UserID FROM Users WHERE Username = %s AND Password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            user_id = result[0]
            messagebox.showinfo("Success", "Login successful!")
            add_animal(notebook, username)
            load_adoption_page(notebook, username, user_id)
        else:
            messagebox.showwarning("Warning", "Invalid username or password!")
    except ms.Error as err:
        messagebox.showerror("Database Error", f"Error during login: {str(err)}")
    finally:
        if mycon:
            cursor.close()
            mycon.close()

# Function to add animal to shelter
def add_animal(notebook, username):
    add_animal_frame = tk.Frame(notebook)
    notebook.add(add_animal_frame, text="Add Animal")

    # Current Date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Title Label
    tk.Label(add_animal_frame, text="Add Animal to Shelter", font=("Helvetica", 16)).pack(pady=10)

    # Animal Name
    tk.Label(add_animal_frame, text="Name:").pack(pady=5)
    name_entry = tk.Entry(add_animal_frame)
    name_entry.pack(pady=5)

    # Species
    tk.Label(add_animal_frame, text="Species:").pack(pady=5)
    species_entry = tk.Entry(add_animal_frame)
    species_entry.pack(pady=5)

    # Age
    tk.Label(add_animal_frame, text="Age:").pack(pady=5)
    age_entry = tk.Entry(add_animal_frame)
    age_entry.pack(pady=5)

    # Display Current Date
    tk.Label(add_animal_frame, text=f"Date: {current_date}").pack(pady=10)

    # Success Message Frame
    message_frame = tk.Frame(add_animal_frame)
    message_frame.pack(pady=10)
    success_message = tk.Label(message_frame, text="", fg="green")
    success_message.pack()

    # Submit Animal Button
    def submit_animal():
        name = name_entry.get()
        species = species_entry.get()
        age = age_entry.get()
        if name and species and age:
            try:
                mycon = connect_database()
                if mycon is None:
                    return
                cursor = mycon.cursor()
                cursor.execute("INSERT INTO animals(animal_name, animal_species, age) VALUES (%s, %s, %s)",
                               (name, species, age))
                mycon.commit()
                success_message.config(
                    text=f"Success! {name} has been added to the shelter by {username} on {current_date}."
                )
            except ms.Error as err:
                messagebox.showerror("Database Error", f"Error adding animal: {str(err)}")
            finally:
                if mycon:
                    cursor.close()
                    mycon.close()
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    submit_button = tk.Button(add_animal_frame, text="Add Animal", command=submit_animal)
    submit_button.pack(pady=10)

# Adoption process page
def load_adoption_page(notebook, adopter_name, user_id):
    adoption_frame = tk.Frame(notebook)
    notebook.add(adoption_frame, text="Adoption Process")

    # Display the name of the logged-in user
    tk.Label(adoption_frame, text=f"Adopter Name: {adopter_name}").pack(pady=10)

    # Create a frame for available animals
    animals_frame = ttk.LabelFrame(adoption_frame, text="Available Animals for Adoption")
    animals_frame.pack(fill="both", expand="yes", padx=10, pady=10)

    # Add treeview to display animals
    animals_tree = ttk.Treeview(animals_frame, columns=("ID", "Name", "Species", "Age"), show="headings")
    animals_tree.heading("ID", text="ID")
    animals_tree.heading("Name", text="Name")
    animals_tree.heading("Species", text="Species")
    animals_tree.heading("Age", text="Age")
    animals_tree.pack(fill="both", expand=True)

    # Fetch Animals
    try:
        mycon = connect_database()
        if mycon is None:
            return
        cursor = mycon.cursor()
        cursor.execute("SELECT * FROM Animals")
        animals_results = cursor.fetchall()
        for animal in animals_results:
            animals_tree.insert('', 'end', values=animal)
    except ms.Error as err:
        messagebox.showerror("Database Error", f"Error fetching animals: {str(err)}")
    finally:
        if mycon:
            cursor.close()
            mycon.close()

    # Adoption Entry Frame
    adoption_entry_frame = tk.Frame(adoption_frame)
    adoption_entry_frame.pack(pady=10)

    # Automatically set the adoption date to today
    tk.Label(adoption_entry_frame, text="Adoption Date (YYYY-MM-DD):").pack()
    adoption_date = datetime.now().strftime("%Y-%m-%d")
    tk.Label(adoption_entry_frame, text=adoption_date).pack()

    # Create "Record Adoption" button
    add_adoption_button = tk.Button(
        adoption_entry_frame, text="Record Adoption",
        command=lambda: add_adoption(animals_tree, adopter_name, adoption_date, user_id)
    )
    add_adoption_button.pack(pady=5)

    # Create a frame for the adoptions table
    adoptions_frame = ttk.LabelFrame(adoption_frame, text="Previous Adoptions")
    adoptions_frame.pack(fill="both", expand="yes", padx=10, pady=10)

    # Treeview to display adoptions
    adoptions_tree = ttk.Treeview(adoptions_frame, columns=("Adopter Name", "Animal Name", "Adoption Date"), show="headings")
    adoptions_tree.heading("Adopter Name", text="Adopter Name")
    adoptions_tree.heading("Animal Name", text="Animal Name")
    adoptions_tree.heading("Adoption Date", text="Adoption Date")
    adoptions_tree.pack(fill="both", expand=True)

    # Load previous adoptions from the database
    load_previous_adoptions(adoptions_tree)

    # Function to record an adoption
    def add_adoption(animals_tree, adopter_name, adoption_date, user_id):
        selected_item = animals_tree.selection()  # Get selected animal
        if selected_item:
            animal_data = animals_tree.item(selected_item, 'values')
            animal_name = animal_data[1]  # Get the selected animal name
            animal_id = animal_data[0]

            try:
                mycon = connect_database()
                if mycon is None:
                    return
                cursor = mycon.cursor()
                cursor.execute("DELETE FROM Animals WHERE id = %s", (animal_id,))
                cursor.execute(
                    "INSERT INTO Adopters (UserID, AdopterName, AnimalName, AdoptionDate) VALUES (%s, %s, %s, %s)",
                    (user_id, adopter_name, animal_name, adoption_date)
                )
                mycon.commit()
                animals_tree.delete(selected_item)
                adoptions_tree.insert("", "end", values=(adopter_name, animal_name, adoption_date))
                messagebox.showinfo("Adoption Recorded", f"{animal_name} adopted by {adopter_name} on {adoption_date}!")
            except ms.Error as err:
                messagebox.showerror("Database Error", f"Error during adoption: {str(err)}")
            finally:
                if mycon:
                    cursor.close()
                    mycon.close()
        else:
            messagebox.showwarning("Input Error", "Please select an animal.")

def load_previous_adoptions(tree):
    try:
        mycon = connect_database()
        if mycon is None:
            return
        cursor = mycon.cursor()
        cursor.execute('''SELECT AdopterName, AnimalName, AdoptionDate FROM Adopters''')
        previous_adoptions = cursor.fetchall()

        tree.delete(*tree.get_children())  # Clear the treeview
        for adoption in previous_adoptions:
            tree.insert("", "end", values=adoption)
    except ms.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if mycon:
            cursor.close()
            mycon.close()

# Function for displaying global data and graphs
def global_data(notebook):
    frame = tk.Frame(notebook)
    notebook.add(frame, text="Global Data")

    # First Treeview for Global Data
    columns1 = ('ID', 'Metric', 'Value')
    tree1 = ttk.Treeview(frame, columns=columns1, show='headings')

    for col in columns1:
        tree1.heading(col, text=col)
        tree1.column(col, anchor="center")

    scrollbar1 = ttk.Scrollbar(frame, orient="vertical", command=tree1.yview)
    tree1.configure(yscroll=scrollbar1.set)
    scrollbar1.pack(side='right', fill='y')

    tree1.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    fetch_global_data(tree1)

    # Second Treeview for Additional Data
    columns2 = ('ID', 'Term', 'Definition')
    tree2 = ttk.Treeview(frame, columns=columns2, show='headings')

    for col in columns2:
        tree2.heading(col, text=col)
        tree2.column(col, anchor="center")

    scrollbar2 = ttk.Scrollbar(frame, orient="vertical", command=tree2.yview)
    tree2.configure(yscroll=scrollbar2.set)
    scrollbar2.pack(side='right', fill='y')

    tree2.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    fetch_additional_data(tree2)

    # Graph buttons
    btn_vulnerable = tk.Button(frame, text="Vulnerable Animals Graph", command=show_vulnerable_graph)
    btn_adoptions = tk.Button(frame, text="Adoptions Graph", command=show_adoptions_graph)
    btn_species = tk.Button(frame, text="Species Graph", command=show_scatter_graph)

    btn_vulnerable.pack(pady=5)
    btn_adoptions.pack(pady=5)
    btn_species.pack(pady=5)

def fetch_global_data(tree):
    try:
        mycon = connect_database()
        if mycon is None:
            return
        cursor = mycon.cursor()
        cursor.execute("SELECT * FROM Global_data")
        results = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in results:
            tree.insert("", tk.END, values=row)
    except ms.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if mycon:
            cursor.close()
            mycon.close()

def fetch_additional_data(tree):
    try:
        mycon = connect_database()
        if mycon is None:
            return
        cursor = mycon.cursor()
        cursor.execute("SELECT * FROM Terms")
        results = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in results:
            tree.insert("", tk.END, values=row)
    except ms.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if mycon:
            cursor.close()
            mycon.close()

def show_vulnerable_graph():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    vulnerable_animals = [15, 20, 25, 30, 28, 35, 40, 42, 40, 44, 37, 40]

    plt.figure(figsize=(10, 5))
    plt.plot(months, vulnerable_animals, marker='', linestyle='--', color='r')
    plt.title('Vulnerable Animals Over Time')
    plt.xlabel('Months')
    plt.ylabel('Number of Vulnerable Animals')
    plt.grid()
    plt.show()

def show_adoptions_graph():
    months = np.array(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    dogs_adopted = np.array([5, 6, 7, 8, 10, 12, 11, 13, 15, 14, 16, 18])
    cats_adopted = np.array([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15])

    plt.figure(figsize=(10, 6))
    plt.plot(months, dogs_adopted, label='Dogs Adopted', marker='o', color='blue')
    plt.plot(months, cats_adopted, label='Cats Adopted', marker='o', color='green')

    plt.title('Monthly Animal Adoptions at the Shelter')
    plt.xlabel('Months')
    plt.ylabel('Number of Animals Adopted')
    plt.legend()
    plt.grid(True)
    plt.show()

def show_scatter_graph():
    species = [
        'Dogs', 'Cats', 'Rabbits', 'Birds (Parrots)',
        'Turtles', 'Hamsters', 'Ferrets',
        'Guinea Pigs', 'Lizards', 'Macaw',
        'Tortoise', 'Red-Footed Tortoise', 'Cockatoo',
        'Green Iguana', 'Beagle'
    ]
    lifespan = [12, 15, 8, 50, 100, 2, 6, 5, 5, 60, 80, 70, 50, 70, 15]
    offspring = [6, 4, 5, 3, 2, 7, 6, 3, 2, 2, 2, 4, 2, 3, 5]

    plt.figure(figsize=(12, 8))
    colors = ['salmon', 'red', 'orange', 'purple',
              'turquoise', 'brown', 'orchid', 'cyan', 'magenta',
              'darkgreen', 'olive', 'chocolate', 'darkgrey', 'navy', 'lightgreen']
    sizes = [100, 80, 50, 200, 20, 40, 60, 30, 25, 100, 20, 40, 100, 60, 20]

    plt.scatter(lifespan, offspring, color=colors, s=sizes, alpha=0.7)

    # Add annotations for each point
    for i, s in enumerate(species):
        plt.annotate(s, (lifespan[i], offspring[i]), textcoords="offset points", xytext=(0, 5), ha='center')

    plt.title('Animal Species: Lifespan vs Offspring')
    plt.xlabel('Average Lifespan (years)')
    plt.ylabel('Average Offspring per Litter')
    plt.grid(False)
    plt.show()

# Main Application
def main():
    root = tk.Tk()
    root.title("Happy Paws Shelter")

    # Create a notebook (tabs)
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Create tabs
    homepage(notebook)
    shelter_data(notebook)
    global_data(notebook)

    # Create registration/login frame
    login_frame = tk.Frame(notebook)
    notebook.add(login_frame, text="Login / Register")

    # Username and password entry
    tk.Label(login_frame, text="Username:").pack()
    username_entry = tk.Entry(login_frame)
    username_entry.pack()

    tk.Label(login_frame, text="Password:").pack()
    password_entry = tk.Entry(login_frame, show='*')
    password_entry.pack()

    register_button = tk.Button(
        login_frame, text="Register",
        command=lambda: register_user(username_entry.get(), password_entry.get(), notebook)
    )
    login_button = tk.Button(
        login_frame, text="Login",
        command=lambda: login_user(username_entry.get(), password_entry.get(), notebook)
    )

    register_button.pack(pady=5)
    login_button.pack(pady=5)

    root.mainloop()

main()
