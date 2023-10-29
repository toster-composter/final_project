import tkinter as tk
from tkinter import ttk
import sqlite3

# Основной класс приложения
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = DB()
        self.view_record()

    # Инициализация главного окна
    def init_main(self):
        tool_bar = tk.Frame(bg='#d7d8e0', bd=2)
        tool_bar.pack(side=tk.TOP, fill=tk.X)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'number', 'email'), height=45, show='headings')
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scroll.set)

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('number', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('number', text='tel. number')
        self.tree.heading('email', text='E-mail')
        self.tree.pack(side=tk.LEFT)

        self.add_img = tk.PhotoImage(file='test_project/img/add.png')
        btn_open_dialog = tk.Button(tool_bar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_png = tk.PhotoImage(file='test_project/img/change.png')
        btn_edit = tk.Button(tool_bar, bg='#d7d8e0', bd=0, image=self.update_png, command=self.open_editor)
        btn_edit.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='test_project/img/delete.png')
        btn_delete = tk.Button(tool_bar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_record)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='test_project/img/search.png')
        btn_search = tk.Button(tool_bar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='test_project/img/refresh.png')
        btn_refresh = tk.Button(tool_bar, bg='#d7d8e0', bd=0, image=self.refresh_img, command=self.view_record)
        btn_refresh.pack(side=tk.LEFT)

    # Открывает диалог для добавления записи
    def open_dialog(self):
        NewWindow()

    # Записывает данные в базу данных и обновляет отображение
    def record(self, name, tel, email):
        self.db.insert_data(name, tel, email)
        self.view_record()

    # Отображает все записи из базы данных в таблице
    def view_record(self):
        self.db.cur.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    # Открывает диалог для редактирования записи
    def open_editor(self):
        Update()

    # Обновляет запись в базе данных и обновляет отображение
    def update_record(self, name, tel, email):
        self.db.cur.execute('''UPDATE db SET name = ?, tel = ?, email = ? WHERE id = ?''',
                            (name, tel, email, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_record()

    # Удаляет запись из базы данных и обновляет отображение
    def delete_record(self):
        for select_item in self.tree.selection():
            self.db.cur.execute('DELETE FROM db WHERE id = ?', self.tree.set(select_item, '#1'))
        self.db.conn.commit()
        self.view_record()

    # Открывает диалог для поиска записи
    def open_search(self):
        Search()

    # Выполняет поиск по записям и обновляет отображение
    def search_contact(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute('SELECT * FROM db WHERE name LIKE ?', (name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]


# Диалог для добавления записи
class NewWindow(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_new_window()
        self.view = app

    def init_new_window(self):
        self.title('ADD')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='tel. number')
        label_select.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_number = ttk.Entry(self)
        self.entry_number.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)

        self.btn_cancel = ttk.Button(self, text='close', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='add')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.record(self.entry_name.get(),
                         self.entry_number.get(),
                         self.entry_email.get()))
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')


# Диалог для редактирования записи
class Update(NewWindow):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.view = app
        self.db = db

    def init_update(self):
        self.title('Edit contact')

        btn_edit = ttk.Button(self, text='Edit')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                      self.entry_number.get(),
                      self.entry_email.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.cur.execute('SELECT * FROM db WHERE id = ?', (self.view.tree.set(self.view.tree.selection()[0], '#1')))
        row = self.db.cur.fetchall()
        self.entry_name.insert(0, row[1])
        self.entry_number.insert(0, row[2])
        self.entry_email.insert(0, row[3])


# Диалог для поиска записи
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Search for contact')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Name')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='close', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Search')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event:
                         self.view.search_contact(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event:
                         self.destroy(), add='+')


# Класс для работы с базой данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('test_db.db')
        self.cur = self.conn.cursor()
        self.table = self.cur.execute('''
        CREATE TABLE IF NOT EXISTS db (
            id INTEGER PRIMARY KEY,
            name TEXT,
            tel TEXT,
            email TEXT
            );
        ''')
        self.conn.commit()

    def insert_data(self, name, tel, email):
        self.cur.execute('INSERT INTO db (name, tel, email) VALUES (?, ?, ?);', (name, tel, email))
        self.conn.commit()

if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()

    root.title('number book')
    root.geometry('650x450')
    root.resizable(False, False)
    root.mainloop()
