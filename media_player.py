import vlc
import tkinter as tk
from pytube import YouTube
import connector

class YouTubePlayer:
    def __init__(self, url, master):
        self.url = url
        self.master = master
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.media_player.set_hwnd(self.get_frame_id())
        self.media = None

    def get_youtube_stream_url(self):
        yt = YouTube(self.url)
        video_stream = yt.streams.filter(file_extension="mp4", res="720p").first()
        if video_stream is None:
            video_stream = yt.streams.filter(file_extension="mp4").first()
        return video_stream.url

    def play(self):
        if not self.media:
            self.media = self.instance.media_new(self.get_youtube_stream_url())
            self.media_player.set_media(self.media)
        self.media_player.play()

    def pause(self):
        self.media_player.pause()

    def resume(self):
        self.media_player.set_pause(0)

    def get_frame_id(self):
        return self.master.winfo_id()

class YouTubePlayerApp:
    def __init__(self, master, player):
        self.master = master
        self.master.title("YouTube Player")

        self.container = tk.Frame(master)
        self.container.pack()

        self.player = player

        self.player.play()

        menubar = tk.Menu(master)
        master.config(menu=menubar)

        playback_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Playback", menu=playback_menu)
        playback_menu.add_command(label="Pause", command=self.pause)
        playback_menu.add_command(label="Resume", command=self.resume)

    def pause(self):
        self.player.pause()

    def resume(self):
        self.player.resume()

def run_youtube_player():
    youtube_url = connector.video_url_mov()

    root = tk.Tk()

    player = YouTubePlayer(youtube_url, root)

    app = YouTubePlayerApp(root, player)

    root.mainloop()

