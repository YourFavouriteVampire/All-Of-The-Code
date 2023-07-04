import tkinter as tk
from tkinter import filedialog
import vlc

class MediaPlayer:
    def __init__(self, master):
        self.master = master
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.muted = False
        self.playback_speeds = [1.0, 2.0, 3.0, 0.5]
        self.current_speed_index = 0
        self.paused = False
        self.is_fullscreen = False

        self.create_widgets()

    def create_widgets(self):
        self.master.title("Media Player")
        self.master.geometry("800x600")
        self.master.config(bg="black")

        self.video_frame = tk.Frame(self.master)
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.master, bg="black")
        self.button_frame.pack(side=tk.BOTTOM, pady=5)

        self.open_button = tk.Button(
            self.button_frame,
            text="Open File",
            command=self.open_file,
            relief=tk.FLAT,
            bg="#555555",
            fg="white",
            activebackground="#777777",
            activeforeground="white",
            padx=10,
            pady=5,
        )
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.seek_backward_button = tk.Button(
            self.button_frame,
            text="Seek Backward 10s",
            command=self.seek_backward,
            relief=tk.FLAT,
            bg="#555555",
            fg="white",
            activebackground="#777777",
            activeforeground="white",
            padx=10,
            pady=5,
        )
        self.seek_backward_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(
            self.button_frame,
            text="Pause",
            command=self.toggle_pause,
            relief=tk.FLAT,
            bg="#555555",
            fg="white",
            activebackground="#777777",
            activeforeground="white",
            padx=10,
            pady=5,
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.seek_forward_button = tk.Button(
            self.button_frame,
            text="Seek Forward 10s",
            command=self.seek_forward,
            relief=tk.FLAT,
            bg="#555555",
            fg="white",
            activebackground="#777777",
            activeforeground="white",
            padx=10,
            pady=5,
        )
        self.seek_forward_button.pack(side=tk.LEFT, padx=5)

        self.playback_speed_button = tk.Button(
            self.button_frame,
            text="1x",
            command=self.toggle_playback_speed,
            relief=tk.FLAT,
            bg="#555555",
            fg="white",
            activebackground="#777777",
            activeforeground="white",
            padx=10,
            pady=5,
        )
        self.playback_speed_button.pack(side=tk.LEFT, padx=5)

        self.fullscreen_button = tk.Button(
            self.button_frame,
            text="Fullscreen",
            command=self.toggle_fullscreen,
            relief=tk.FLAT,
            bg="#555555",
            fg="white",
            activebackground="#777777",
            activeforeground="white",
            padx=10,
            pady=5,
        )
        self.fullscreen_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(
            self.button_frame,
            text="Stop",
            command=self.stop_media,
            relief=tk.FLAT,
            bg="#555555",
            fg="white",
            activebackground="#777777",
            activeforeground="white",
            padx=10,
            pady=5,
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.mute_button = tk.Button(
            self.button_frame,
            text="Mute",
            command=self.toggle_mute,
            relief=tk.FLAT,
            bg="#555555",
            fg="white",
            activebackground="#777777",
            activeforeground="white",
            padx=10,
            pady=5,
        )
        self.mute_button.pack(side=tk.LEFT, padx=5)

        self.volume_slider = tk.Scale(
            self.button_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=100,
            sliderrelief=tk.FLAT,
            bg="black",
            fg="white",
            activebackground="#777777",
            highlightthickness=0,
            command=self.set_volume,
        )
        self.volume_slider.set(100)
        self.volume_slider.pack(side=tk.LEFT, padx=5)

        self.volume_label = tk.Label(
            self.button_frame,
            text="Volume",
            bg="black",
            fg="white",
        )
        self.volume_label.pack(side=tk.LEFT, padx=5)

        self.master.bind("<Left>", lambda event: self.seek_backward())
        self.master.bind("<Right>", lambda event: self.seek_forward())
        self.master.bind("<Up>", lambda event: self.change_volume(5))
        self.master.bind("<Down>", lambda event: self.change_volume(-5))
        self.master.bind("<m>", lambda event: self.toggle_mute_keyboard())
        self.master.bind("<space>", lambda event: self.toggle_pause())
        self.master.bind("<Escape>", lambda event: self.toggle_fullscreen())

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("All Files", "*.*"),
            ]
        )
        if file_path:
            self.play_media(file_path)

    def play_media(self, file_path):
        media = self.instance.media_new(file_path)
        self.player.set_media(media)

        self.player.set_hwnd(self.video_frame.winfo_id())
        self.player.play()

    def toggle_pause(self, event=None):
        if self.paused:
            self.player.play()
            self.paused = False
            self.pause_button.config(text="Pause")
        else:
            self.player.pause()
            self.paused = True
            self.pause_button.config(text="Resume")

    def seek_forward(self, event=None):
        current_time = self.player.get_time()
        self.player.set_time(current_time + 10000)

    def seek_backward(self, event=None):
        current_time = self.player.get_time()
        self.player.set_time(current_time - 10000)

    def stop_media(self):
        self.player.stop()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.master.attributes("-fullscreen", self.is_fullscreen)
        if self.is_fullscreen:
            self.button_frame.pack_forget()
        else:
            self.button_frame.pack(side=tk.BOTTOM, pady=5)

    def toggle_mute(self):
        self.muted = not self.muted
        self.player.audio_set_mute(self.muted)

        if self.muted:
            self.mute_button.config(text="Unmute")
        else:
            self.mute_button.config(text="Mute")

    def toggle_mute_keyboard(self, event=None):
        self.toggle_mute()

    def set_volume(self, value):
        self.player.audio_set_volume(int(value))

    def change_volume(self, amount):
        current_volume = self.player.audio_get_volume()
        new_volume = current_volume + amount

        if new_volume < 0:
            new_volume = 0
        elif new_volume > 100:
            new_volume = 100

        self.player.audio_set_volume(new_volume)
        self.volume_slider.set(new_volume)

    def toggle_playback_speed(self):
        self.current_speed_index = (self.current_speed_index + 1) % len(self.playback_speeds)
        speed = self.playback_speeds[self.current_speed_index]
        self.player.set_rate(speed)
        self.playback_speed_button.config(text=f"{speed}x")

root = tk.Tk()
media_player = MediaPlayer(root)
root.mainloop()
