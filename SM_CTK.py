import customtkinter as c
from customtkinter import *
from tkinter import ttk, messagebox
import sqlite3

# Ensure the Student table exists
d = sqlite3.connect("student.db")
cursor = d.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Student(
        ID TEXT PRIMARY KEY,
        NAME VARCHAR(20),
        AGE TEXT,
        DOB VARCHAR(25),
        GENDER VARCHAR(10),
        CITY VARCHAR(50)
    )
""")
d.commit()
d.close()


class Student:
    def __init__(self, root):
        self.root = root

        # Top Frame
        self.frame_1 = CTkFrame(self.root, fg_color="red", width=1200, height=50)
        self.frame_1.pack(fill="x")

        self.title = CTkLabel(self.frame_1, text="Student Management System",
                              font=("Arial", 20, "bold"), fg_color="yellow", text_color="black", width=1200)
        self.title.pack(pady=10)

        # Left Frame
        self.frame_2 = CTkFrame(self.root, fg_color="yellow", height=550, width=400, border_width=2, border_color="black")
        self.frame_2.pack(side=LEFT)
        self.frame_2.propagate(0)

        CTkLabel(self.frame_2, text="Student details", font=("Arial", 20)).place(x=20, y=40)

        # Entry Fields
        self.create_label_entry("ID :", 80)
        self.create_label_entry("NAME", 120)
        self.create_label_entry("AGE", 160)
        self.create_label_entry("DOB", 200)
        self.create_label_entry("GENDER", 240)
        self.create_label_entry("CITY", 280)

        # Buttons
        self.add_btn = CTkButton(self.frame_2, text="Add", command=self.add).place(x=120, y=350)
        self.delete_btn = CTkButton(self.frame_2, text="Delete", command=self.delete).place(x=120, y=380)
        self.update_btn = CTkButton(self.frame_2, text="Update", command=self.update).place(x=120, y=410)
        self.clear_btn = CTkButton(self.frame_2, text="Clear", command=self.clear).place(x=120, y=440)

        # Right Frame
        self.frame_3 = CTkFrame(self.root, fg_color="yellow", width=800, height=550, border_color="black", border_width=2)
        self.frame_3.pack(side=RIGHT)

        # YOUR ORIGINAL TREEVIEW SETUP
        self.tree = ttk.Treeview(self.frame_3, columns=("c1", "c2", "c3", "c4", "c5", "c6"), height=25, show="headings")
        self.tree.pack()

        self.tree.column("#1", anchor=CENTER, width=80)
        self.tree.heading("#1", text="ID")

        self.tree.column("#2", anchor=CENTER, width=120)
        self.tree.heading("#2", text="NAME")

        self.tree.column("#3", anchor=CENTER, width=120)
        self.tree.heading("#3", text="Age")

        self.tree.column("#4", anchor=CENTER, width=160)
        self.tree.heading("#4", text="Dob")

        self.tree.column("#5", anchor=CENTER, width=160)
        self.tree.heading("#5", text="GENDER")

        self.tree.column("#6", anchor=CENTER, width=200)
        self.tree.heading("#6", text="CITY")

        # Bind selection
        self.tree.bind("<ButtonRelease-1>", self.select_item)

        # Load data from DB
        self.load_data()

    def create_label_entry(self, text, y_pos):
        label = CTkLabel(self.frame_2, text=text, font=("Arial", 15))
        label.place(x=50, y=y_pos)
        entry = CTkEntry(self.frame_2, width=200)
        entry.place(x=120, y=y_pos)
        setattr(self, f"{text.split()[0].lower()}_entry", entry)

    def load_data(self):
        d = sqlite3.connect("student.db")
        cursor = d.cursor()
        cursor.execute("SELECT * FROM Student")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", END, values=row)
        d.close()

    def add(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        dob = self.dob_entry.get()
        gender = self.gender_entry.get()
        city = self.city_entry.get()

        if not id or not name or not age or not gender or not city:
            messagebox.showwarning("Alert", "Please fill all the details")
            return

        try:
            d = sqlite3.connect("student.db")
            cursor = d.cursor()
            cursor.execute("INSERT INTO Student (ID, NAME, AGE, DOB, GENDER, CITY) VALUES (?, ?, ?, ?, ?, ?)",
                           (id, name, age, dob, gender, city))
            d.commit()
            d.close()
            self.tree.insert("", END, values=(id, name, age, dob, gender, city))
            self.clear()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student ID already exists!")

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Alert", "Please select a student to delete")
            return
        student_id = self.tree.item(selected[0])['values'][0]
        self.tree.delete(selected[0])

        d = sqlite3.connect("student.db")
        cursor = d.cursor()
        cursor.execute("DELETE FROM Student WHERE ID=?", (student_id,))
        d.commit()
        d.close()
        self.clear()

    def update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Alert", "Please select a student to update")
            return

        id = self.id_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        dob = self.dob_entry.get()
        gender = self.gender_entry.get()
        city = self.city_entry.get()

        self.tree.item(selected[0], values=(id, name, age, dob, gender, city))

        d = sqlite3.connect("student.db")
        cursor = d.cursor()
        cursor.execute("""
            UPDATE Student SET NAME=?, AGE=?, DOB=?, GENDER=?, CITY=? WHERE ID=?
        """, (name, age, dob, gender, city, id))
        d.commit()
        d.close()
        self.clear()

    def clear(self):
        for entry in [self.id_entry, self.name_entry, self.age_entry, self.dob_entry, self.gender_entry, self.city_entry]:
            entry.delete(0, END)

    def select_item(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        if values:
            self.id_entry.delete(0, END)
            self.id_entry.insert(0, values[0])
            self.name_entry.delete(0, END)
            self.name_entry.insert(0, values[1])
            self.age_entry.delete(0, END)
            self.age_entry.insert(0, values[2])
            self.dob_entry.delete(0, END)
            self.dob_entry.insert(0, values[3])
            self.gender_entry.delete(0, END)
            self.gender_entry.insert(0, values[4])
            self.city_entry.delete(0, END)
            self.city_entry.insert(0, values[5])


# Main window
root = c.CTk()
root.geometry("1200x600")
root.title("Blackops Student Management System")
root.resizable(False, False)
root._set_appearance_mode("dark")

app = Student(root)
root.mainloop()
