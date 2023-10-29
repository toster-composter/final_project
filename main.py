import tkinter as tk
from tkinter import ttk
import sqlite3

# Main application class
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = DB()
        self.view_record()

    # Initialize the main window and UI components
    def init_main(self):
        # Create a toolbar
        tool_bar = tk.Frame(bg='#d7d8e0', bd=2)
        tool_bar.pack(side=tk.TOP, fill=tk.X)

        # Create a Treeview widget for displaying records
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'number', 'email', 'salary'), height=45, show='headings')
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scroll.set)

        # Define columns and headings for the Treeview
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('number', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=200, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('number', text='Номер тел.')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')
        self.tree.pack(side=tk.LEFT)

        # Create buttons for various operations
        self.add_img = tk.PhotoImage(file='img/add.png')
        btn_open_dialog = tk.Button(tool_bar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_png = tk.PhotoImage(file='img/change.png')
        btn_edit = tk.Button(tool_bar, bg='#d7d8e0', bd=0, image=self.update_png, command=self.open_editor)
        btn_edit.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='img/delete.png')
        btn_delete = tk.Button(tool_bar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_record)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='img/search.png')
        btn_search = tk.Button(tool_bar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='test_project/img/refresh.png')
        btn_refresh = tk.Button(tool_bar, bg='#d7d8e0', bd=0, image=self.refresh_img, command=self.view_record)
        btn_refresh.pack(side=tk.LEFT)

    # Open a dialog to add a new record
    def open_dialog(self):
        NewWindow()

    # Record data to the database and refresh the view
    def record(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_record()

    # Display all records from the database in the table
    def view_record(self):
        self.db.cur.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    # Open a dialog to edit a record
    def open_editor(self):
        Update()

    # Update a record in the database and refresh the view
    def update_record(self, name, tel, email, salary):
        self.db.cur.execute('''UPDATE db SET name = ?, tel = ?, email = ?, salary = ? WHERE id = ?''',
                            (name, tel, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_record()

    # Delete a record from the database and refresh the view
    def delete_record(self):
        for select_item in self.tree.selection():
            self.db.cur.execute('DELETE FROM db WHERE id = ?', self.tree.set(select_item, '#1'))
        self.db.conn.commit()
        self.view_record()

    # Open a dialog to search for a record
    def open_search(self):
        Search()

    # Search for records and refresh the view
    def search_employee(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute('SELECT * FROM db WHERE name LIKE ?', (name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

# Dialog for adding a record
class NewWindow(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_new_window()
        self.view = app

    # Initialize the dialog for adding a new record
    def init_new_window(self):
        self.title('Добавить сотрудника')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # Labels and entry fields for user input
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Номер тел.')
        label_select.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_number = ttk.Entry(self)
        self.entry_number.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        # Buttons for adding and closing the dialog
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.record(self.entry_name.get(),
                         self.entry_number.get(),
                         self.entry_email.get(),
                         self.entry_salary.get()))
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')

# Dialog for editing a record
class Update(NewWindow):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.view = app
        self.db = db

    # Initialize the dialog for updating a record
    def init_update(self):
        self.title('Изменить сотрудника')

        btn_edit = ttk.Button(self, text='Изменить')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                      self.entry_number.get(),
                      self.entry_email.get(),
                      self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    # Populate the fields with the data of the selected record
    def default_data(self):
        self.db.cur.execute('SELECT * FROM db WHERE id = ?', (self.view.tree.set(self.view.tree.selection()[0], '#1')))
        row = self.db.cur.fetchall()
        self.entry_name.insert(0, row[1])
        self.entry_number.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

# Dialog for searching for a record
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    # Initialize the search dialog
    def init_search(self):
        self.title('Искать сотрудника')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Имя')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Искать')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event:
                         self.view.search_employee(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event:
                         self.destroy(), add='+')

# Database class
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('MAIN_db.db')
        self.cur = self.conn.cursor()
        self.table = self.cur.execute('''
        CREATE TABLE IF NOT EXISTS db (
            id INTEGER PRIMARY KEY,
            name TEXT,
            tel TEXT,
            email TEXT,
            salary TEXT
            );
        ''')
        self.conn.commit()

    # Insert data into the database
    def insert_data(self, name, tel, email, salary):
        self.cur.execute('INSERT INTO db (name, tel, email, salary) VALUES (?, ?, ?, ?);', (name, tel, email, salary))
        self.conn.commit()

if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()

    root.title('Список сотрудников компании')
    root.geometry('840x450')
    root.resizable(False, False)
    root.mainloop()
