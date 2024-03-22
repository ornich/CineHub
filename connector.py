import mysql.connector as sql
import datetime
import wikipedia

conx = sql.connect(host="localhost", user='root', passwd='myroot2006', database="nithil")

cusr = conx.cursor()


def security_qna(user_name, dob):
    try:
        cusr.execute("select * from qna natural join passwd;")
        user = user_name
        q = cusr.fetchall()
        u_pass = False
        for i in q:
            if i[0] == user:
                sec = dob
                if str(i[1]) == sec:
                    u_pass = i[2]
                else:
                    u_pass = False
            else:
                u_pass = False
        return u_pass
    except:
        print("Error at security_qna")


def verify(user, passwd):
    try:
        cusr.execute("select * from passwd")
        rec = cusr.fetchall()
        found = 0
        c_pass = 0
        for i in rec:
            if i[0] == user:
                if i[1] == passwd:
                    found = 1
                    c_pass = 1
                    break
                else:
                    found = 1
                    break
            else:
                found = 0
        if found == 0:
            pass
        return found, c_pass
    except:
        print("Error at verify")


def admin_check(user):
    try:
        cusr.execute("select * from passwd")
        rec = cusr.fetchall()
        cond = False
        username = user
        for i in rec:
            if i[0] == username:
                if i[2] == 'y':
                    cond = True
                    break
        return cond
    except:
        print("Error at admin_check")


def username_generater(username_get):
    try:
        username = username_get
        cond = False

        cusr.execute("Select username from passwd")
        rec = cusr.fetchall()
        for i in rec:
            for j in i:
                if username == j:
                    cond = True
        return cond
    except:
        print("Error at username_generater")


def create  (username, password, dobc):
    try:
        create_user = username
        dob = dobc
        passwd = password
        form = (create_user, passwd)
        cusr.execute("insert into passwd(username,password) values{};".format(form))
        conx.commit()
        form = (create_user, dob)
        cusr.execute("insert into qna values{}".format(form))
        conx.commit()
    except:
        print("Error at create")


def add_mov(name_movie, picture, yor, rating, category, actor, director, premium_check, link):
    try:
        cusr.execute("select id from admin_table")
        rec = cusr.fetchall()
        count = 0
        for i in rec:
            for j in i:
                count = j + 1
        name = name_movie
        img = picture
        year = yor
        rating = rating
        cat = category
        act = actor
        director = director
        if premium_check == "No":
            premium_check = "NULL"
        else:
            premium_check = "t"

        cusr.execute(
            "insert into admin_table values({},'{}','{}','{}','{}','{}','{}','{}',NULL,'{}','{}')".format(count, name,
                                                                                                          img,
                                                                                                          year, rating,
                                                                                                          cat,
                                                                                                          act, director,
                                                                                                          premium_check,
                                                                                                          link))
        conx.commit()

    except:
        print("Error at add_mov")


def del_mov(id_del_admin):
    try:
        cusr.execute("select distinct id from admin_table")
        id_del = id_del_admin
        rc = cusr.fetchall()
        cond = False
        for i in rc:
            for j in i:
                if j == id_del:
                    cusr.execute("delete from admin_table where id = {};".format(id_del))
                    conx.commit()
                    cond = True
                    break
        return cond
    except:
        print("Error at del_mov")


def del_date_mov(mov_id, del_date):
    try:
        cusr.execute('update admin_table set del_date = "{}" where id = {}'.format(del_date, int(mov_id)))
        conx.commit()
        return True
    except:
        print("Error at del_date_mov")


def del_check():
    date = datetime.date.today()
    cusr.execute("delete from admin_table where del_date <= '{}';".format(date))
    conx.commit()


def main_img_premium():
    cusr.execute("Select * from admin_table")
    rec = cusr.fetchall()
    movies = []
    for i in rec:
        dict_mov = {}
        dict_mov["image_url"] = i[2]
        dict_mov["name"] = i[1]
        movies.append(dict_mov)
    return movies


def view_rec():
    cusr.execute("select * from members")
    rec = cusr.fetchall()
    header = ("Id", "Username", "Name", "Phone Number", "Premium")
    rec.insert(0, header)
    return rec


def premium(username):
    un = username
    cusr.execute("select * from members")
    members = cusr.fetchall()
    for i in members:
        if i[1] == un:
            if i[4] == 'y':
                return True
                break
            else:
                return False


def video_url_mov():
    cusr.execute("Select * from admin_table where name = '{}'".format(movie_name))
    rec = cusr.fetchall()
    rec = rec[0][-1]
    return rec


def premium_payment(username):
    try:
        cusr.execute("update members set premium = 'y' where username = '{}';".format(username))
        conx.commit()
        return True
    except:
        return False

def act_dir_detail():
    cusr.execute(
        "select Actors, Director,  Category, rating, premium from admin_table where name = '{}'".format(movie_name))
    rec = cusr.fetchall()
    return rec


def movie_detail(mov_detail):
    global movie_name
    movie_name = mov_detail
    mov_name = mov_detail + " Film"
    information = wikipedia.summary(mov_name, 4)
    info_split = information.split(".")
    return info_split


def members_insert(username, name, phone):
    cusr.execute("select user_id from members")
    rec = cusr.fetchall()
    counter = rec[-1][-1]+1
    values = (counter, username, name, phone, 'n')
    cusr.execute("insert into members value{}".format(values))
    conx.commit()

