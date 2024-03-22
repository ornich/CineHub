import connector
from tkinter import *
from tkinter import messagebox
import admin_page
import premium_page
import user_page_cinehub


def create_fn():
    pass_get = password.get()
    repass_get = re_password.get()
    username_get = username.get()
    dobcreate_get = dob_create.get()
    name_get = name.get()
    phone_get = phone.get()
    if connector.username_generater(username_get) == False:
        if pass_get == repass_get:
            connector.members_insert(username_get, name_get, phone_get)
            connector.create(username_get, pass_get, dobcreate_get)
            messagebox.showinfo("Created", "Created Successfully", icon='info')
            create_window.destroy()
            login_win()
        else:
            messagebox.showinfo("Error", "Password Did Not Match", icon='error')
    else:
        messagebox.showinfo("Error", "Username Already Exists", icon="error")


def create_win():
    global username
    global password
    global re_password
    global dob_create
    global create_window
    global phone
    global name
    login_window.destroy()
    create_window = Tk()
    create_window.geometry("700x600")
    Label(create_window, text="Username", font=("arial", 25)).grid(row=0)
    Label(create_window, text="Password", font=("arial", 25)).grid(row=5)
    Label(create_window, text="Re-Enter Password", font=("arial", 25)).grid(row=10)
    Label(create_window, text="DOB (yyyy-mm-dd)", font=("arial", 25)).grid(row=15)
    Label(create_window,text="Name",font=("arial", 25)).grid(row=20)
    Label(create_window,text="Phone",font=("arial",25)).grid(row=25)
    username = Entry(create_window)
    password = Entry(create_window)
    re_password = Entry(create_window)
    dob_create = Entry(create_window)
    name = Entry(create_window)
    phone = Entry(create_window)
    username.grid(row=0, column=1)
    password.grid(row=5, column=1)
    re_password.grid(row=10, column=1)
    dob_create.grid(row=15, column=1)
    name.grid(row=20, column=1)
    phone.grid(row = 25, column=1)
    create = Button(create_window, text='Create', font=("arial", 18), command=create_fn)
    create.grid(row=30, column=1)

    create_window.mainloop()


def forgot_ver():
    ret = connector.security_qna(user_name.get(), dob.get())
    if ret == False:
        messagebox.showinfo("Wrong Input", "Wrong Input")
    else:
        u_pass = "Password Is : " + ret
        messagebox.showinfo("Password", u_pass)
        forgot.destroy()
        login_win()


def forgot_win():
    login_window.destroy()

    global forgot
    global user_name
    global dob
    forgot = Tk()
    forgot.geometry("500x200")

    Label(forgot, text="Username", font=("arial", 30)).grid(row=5)
    Label(forgot, text="DOB (yyyy-mm-dd)", font=("arial", 20)).grid(row=10)
    user_name = Entry(forgot)
    user_name.grid(row=5, column=2)
    dob = Entry(forgot)
    dob.grid(row=10, column=2)
    enter = Button(forgot, text='Enter', font=("arial", 20), command=forgot_ver)
    enter.grid(row=11, column=0)

    forgot.mainloop()


def verifyied():
    ver = connector.verify(user.get(), passwd.get())
    adm = connector.admin_check(user.get())
    pre = connector.premium(user.get())
    if ver[0] == 1:
        if ver[1] == 1:
            login_window.destroy()
            if adm == True:
                admin_page.admin_win()
            else:
                if pre == True:
                    premium_page.main_page()
                else:
                    user_page_cinehub.main_page()
    if ver[0] == 1:
        if ver[1] == 0:
            messagebox.showinfo("Incorrect", "Incorrect Password", icon='error')
    if ver[0] == 0:
        messagebox.showinfo("User Not Found", "User Not Found", icon='error')


def login_win():
    global user
    global passwd
    global login_window
    login_window = Tk()
    login_window.geometry("700x600")

    Label(login_window, text="Login", font=("arial", 30)).grid(row=0, column=1)
    Label(login_window, text="Username", font=("arial", 30)).grid(row=5)
    Label(login_window, text="Password", font=("arial", 30)).grid(row=10)
    user = Entry(login_window)
    passwd = Entry(login_window, show="*")
    user.grid(row=5, column=2)
    passwd.grid(row=10, column=2)
    login = Button(login_window, text='Login', font=("arial", 20), command=verifyied)
    login.grid(row=11, column=0)
    create = Button(login_window, text='Create User', font=("arial", 18), command=create_win)
    create.grid(column=2, row=11)
    link = Label(login_window, text="Forgot Password", fg="blue", cursor="hand2", font=("arial", 14))
    link.grid(row=20, column=1)
    link.bind("<Button-1>", lambda e: forgot_win())

    login_window.mainloop()


connector.del_check()
login_win()
