from tkinter import *
from tkinter import messagebox
from tkinter import ttk as ttk
import connector
from connector import *


def del_movie_win():
    admin_window.destroy()
    global del_window
    del_window = Tk()
    del_window.geometry("400x200")
    Button(del_window, text="Delete Instantly", font=("arial", 15), command=del_inst_win).grid(row=1, column=0)
    Button(del_window, text="Delete Later", font=('arial', 15), command=del_later_win).grid(row=1, column=1)
    Button(del_window, text="Back", font=("arial", 15), command=lambda: [del_window.destroy(), admin_win()]).grid(row=3,column=1,sticky=NE)
    del_window.mainloop()


def create_fn_add():
    add_mov(name.get(), pic.get(), yor.get(), age.get(), cat.get(), act.get(), director.get(), premium_check.get(), link.get())
    messagebox.showinfo("Inserted", "Inserted")
    add_window.destroy()
    admin_win()


def del_later_fn():
    movie_id_get = movie_id.get()
    date_get = date.get()
    print(movie_id_get, date_get)
    connector.del_date_mov(movie_id_get, date_get)
    cond = connector.del_date_mov(movie_id_get, date_get)
    if cond is True:
        messagebox.showinfo("Date is set", "Date is set")
    else:
        messagebox.showerror("Error", "Error on inserting date")


def del_later_win():
    global movie_id, date
    del_later_window = Tk()
    del_later_window.geometry("500x500")
    Label(del_later_window, text="Movie Id", font=("arial", 30)).grid(row=1, column=0)
    Label(del_later_window, text="Date To Delete(yyyy-mm-dd)", font=("arial", 15)).grid(row=2, column=0)
    movie_id = Entry(del_later_window)
    date = Entry(del_later_window)
    movie_id.grid(row=1, column=1)
    date.grid(row=2, column=1)
    Button(del_later_window, text="Delete", font=("arial", 15), command=del_later_fn).grid(row=3, column=1)
    Button(del_later_window, text="Back", font=("arial", 15),
           command=lambda: [del_later_window.destroy(), del_movie_win()]).grid(row=4, column=1)
    del_later_window.mainloop()


def inst_del_fn():
    cond = del_mov(int(mov_id.get()))
    if cond == True:
        messagebox.showinfo("Movie Deleted", "Movie Deleted")
        del_inst_window.destroy()
        admin_win()
    else:
        messagebox.showinfo("Record Not Found", "Movie Id Not Found Check Properly", icon="error")


def sign_out_fn():
    admin_window.destroy()

def del_inst_win():
    global mov_id
    global del_inst_window
    del_window.destroy()
    del_inst_window = Tk()
    del_inst_window.geometry("500x500")
    Label(del_inst_window, text="Movie Id", font=("arial", 30)).grid(row=1, column=0)
    mov_id = Entry(del_inst_window)
    mov_id.grid(row=1, column=1)
    Button(del_inst_window, text="Delete", font=("arial", 15), command=inst_del_fn).grid(row=2, column=1)
    Button(del_inst_window, text="Back", font=("arial", 15),
           command=lambda: [del_inst_window.destroy(), del_movie_win()]).grid(row=3, column=1)
    del_inst_window.mainloop()


def add_movie_win():
    global name, pic, yor, act, director, cat, age, add_window, premium_check, link
    admin_window.destroy()
    add_window = Tk()
    add_window.geometry("700x600")
    Label(add_window, text="Name", font=("arial", 30)).grid(row=1, column=0)
    Label(add_window, text="Picture Link", font=("arial", 30)).grid(row=2, column=0)
    Label(add_window, text="Year Of Release", font=("arial", 30)).grid(row=3, column=0)
    Label(add_window, text="Age Rating", font=("arial", 30)).grid(row=4, column=0)
    Label(add_window, text="Category", font=("arial", 30)).grid(row=5, column=0)
    Label(add_window, text="Actor", font=("arial", 30)).grid(row=6, column=0)
    Label(add_window, text="Director", font=("arial", 30)).grid(row=7, column=0)
    Label(add_window, text="Premium", font=("arial", 30)).grid(row=8,column =0)
    Label(add_window, text="Video Link", font=("arial", 30)).grid(row=9,column = 0)
    age = ttk.Combobox(add_window)
    age["value"] = ['PG', '13+', '16+', 'R-18']
    age.grid(row=4, column=1)
    premium_check = ttk.Combobox(add_window)
    premium_check["value"] = ['Yes', "No"]
    premium_check.grid(row=8, column=1)
    name = Entry(add_window)
    pic = Entry(add_window)
    yor = Entry(add_window)
    cat = Entry(add_window)
    act = Entry(add_window)
    director = Entry(add_window)
    link = Entry(add_window)
    link.grid(row = 9, column = 1)
    name.grid(row=1, column=1)
    pic.grid(row=2, column=1)
    pic.grid(row=2, column=1)
    yor.grid(row=3, column=1)
    cat.grid(row=5, column=1)
    act.grid(row=6, column=1)
    director.grid(row=7, column=1)
    Button(add_window, text="Create", font=('arial', 15), command=create_fn_add).grid(row=10, column=1)
    Button(add_window, text="Back", font=('arial', 15), command=lambda: [add_window.destroy(), admin_win()]).grid(row=11,column=1)

    add_window.mainloop()


class Table:

    def __init__(self, root):

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(root, width=20, font=('Arial', 16, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])



def view_members():
    global total_rows, total_columns, lst
    lst = connector.view_rec()
    total_rows = len(lst)
    total_columns = len(lst[0])

    view_window = Tk()
    Table(view_window)
    view_window.mainloop()


def admin_win():
    global admin_window
    admin_window = Tk()
    admin_window.geometry("700x600")
    Label(admin_window, text="Admin Page", font=("arial", 40)).grid(row=0, column=0)
    Label(admin_window, text="Add Movies", font=("arial", 30)).grid(row=1, column=0)
    Label(admin_window, text="Delete Movies", font=("arial", 30)).grid(row=2, column=0)
    Label(admin_window, text="View Members", font=("arial", 30)).grid(row=3, column=0)
    add_movie = Button(admin_window, text="Add Movies", font=("arial", 15), command=add_movie_win)
    delete_movie = Button(admin_window, text="Delete Movie", font=("arial", 15), command=del_movie_win)
    view_member = Button(admin_window, text="View Members", font=("arial", 15), command=view_members)
    sign_out = Button(admin_window, text="Sign Out", font=("arial", 15),command=sign_out_fn)
    add_movie.grid(row=1, column=1)
    delete_movie.grid(row=2, column=1)
    view_member.grid(row=3, column=1)
    sign_out.grid(row=4, column=1)

    admin_window.mainloop()

