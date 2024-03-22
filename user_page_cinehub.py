import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import connector
import media_player

movies = connector.main_img_premium()
image_width = 200
image_height = 300
movies_per_row = 6



def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))


def premium_submit():
    user_premium_get = username_premium_value.get()
    print(user_premium_get)
    connector.premium_payment(user_premium_get)
    messagebox.showinfo("Completed","Payment is complete. Login again")
    premium_win.destroy()
    root.destroy()

def premium_subscribe():
    global premium_win,username_premium_value
    premium_win = tk.Tk()
    premium_win.title("Payment")
    card = tk.Label(premium_win, text="Card No:", font=("arial", 20))
    card.grid(row=1, column=0)
    exp = tk.Label(premium_win, text="Expire Date:", font=("arial", 20))
    exp.grid(row=2, column=0)
    cvv = tk.Label(premium_win, text="Cvv:", font=("arial", 20))
    cvv.grid(row=3, column=0)
    username_premium = tk.Label(premium_win, text="Username:", font=("arial", 20))
    username_premium.grid(row=4, column=0)
    card_value = tk.Entry(premium_win)
    card_value.grid(row=1, column=1)
    exp_value = tk.Entry(premium_win)
    exp_value.grid(row=2, column=1)
    cvv_value = tk.Entry(premium_win, show="*")
    cvv_value.grid(row=3, column=1)
    username_premium_value = tk.Entry(premium_win)
    username_premium_value.grid(row=4,column=1)
    tk.Button(premium_win, text="Submit", command=premium_submit).grid(row=5, column=1)
    premium_win.mainloop()


def play_fn():
    media_player.run_youtube_player()


def desc_mov(mov_desc):
    text = connector.movie_detail(mov_desc)
    return text


def actor_dir_category():
    detail = connector.act_dir_detail()
    return detail


def show_info(movie_name):
    global movie_name_ref
    mov_desc = desc_mov(movie_name)
    movie_name_ref = movie_name
    act_dir = actor_dir_category()
    actor = "Actor: " + act_dir[0][0]
    director = "Director: " + act_dir[0][1]
    category = "Category: " + act_dir[0][2]
    rating = "Rating: " + act_dir[0][3]
    premium = act_dir[0][4]
    if premium == "t":
        messagebox.showinfo("Premium", "This Movie Is For Premium Users")
    else:
        info = tk.Tk()
        info.title(movie_name)
        main_frame = tk.Frame(info, padx=20, pady=20)
        main_frame.pack()
        play_button = tk.Button(main_frame, text="Play", command=play_fn)
        play_button.pack(side=tk.TOP, pady=10)
        description_text_0 = tk.Label(main_frame, text=mov_desc[0], font=("arial", 10))
        description_text_0.pack(side=tk.TOP, pady=10)
        description_text_1 = tk.Label(main_frame, text=mov_desc[1], font=("arial", 10))
        description_text_1.pack(side=tk.TOP, pady=15)
        description_text_2 = tk.Label(main_frame, text=mov_desc[2], font=("arial", 10))
        description_text_2.pack(side=tk.TOP, pady=20)
        description_text_3 = tk.Label(main_frame, text=mov_desc[3], font=("arial", 10))
        description_text_3.pack(side=tk.TOP, pady=25)
        description_text_4 = tk.Label(main_frame, text=mov_desc[4], font=("arial", 10))
        description_text_4.pack(side=tk.TOP, pady=30)
        actor = tk.Label(main_frame, text=actor, font=("arial", 10))
        actor.pack(side=tk.TOP, pady=35)
        director = tk.Label(main_frame, text=director, font=("arial", 10))
        director.pack(side=tk.TOP, pady=40)
        category = tk.Label(main_frame, text=category, font=("arial", 10))
        category.pack(side=tk.TOP, pady=45)
        rating = tk.Label(main_frame, text=rating, font=("arial", 10))
        rating.pack(side=tk.TOP, pady=50)

        info.mainloop()


def fetch_and_display_images(canvas_frame):
    for i, movie_data in enumerate(movies):
        response = requests.get(movie_data["image_url"])
        if response.status_code == 200:
            image_data = Image.open(BytesIO(response.content))
            image_data = image_data.resize((image_width, image_height))
            movie_image = ImageTk.PhotoImage(image_data)

            movie_frame = tk.Frame(canvas_frame)
            movie_frame.grid(row=i // movies_per_row, column=i % movies_per_row, padx=10)

            movie_label = tk.Label(movie_frame, image=movie_image)
            movie_label.image = movie_image  # Keep a reference to the image
            movie_label.pack()

            movie_name_label = tk.Label(movie_frame, text=movie_data["name"], cursor="hand2")
            movie_name_label.bind("<Button-1>", lambda event, name=movie_data["name"]: show_info(name))
            movie_name_label.pack()


def main_page():
    global canvas
    global root
    root = tk.Tk()
    root.title("CineHub")

    header_frame = tk.Frame(root)
    header_frame.pack()

    sign_out_button = tk.Button(header_frame, text="Premium Subscribe", command=premium_subscribe)
    sign_out_button.pack(side=tk.LEFT, padx=20, pady=10)

    premium_button = tk.Button(header_frame, text="Sign Out", command=root.quit)
    premium_button.pack(side=tk.RIGHT, padx=5, pady=10)
    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=canvas_frame, anchor=tk.NW)

    canvas_frame.bind("<Configure>", on_configure)
    canvas.configure(yscrollcommand=scrollbar.set)

    fetch_and_display_images(canvas_frame)

    root.mainloop()

