import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
from tkinter import ttk

class YoutubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")

        # create entry widget for video url
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.grid(row=0, column=0, padx=10, pady=10)

        # create button to download video
        self.download_button = tk.Button(self.root, text="Download", command=self.download_video)
        self.download_button.grid(row=0, column=2, padx=10, pady=10)

        # create button to select download directory
        self.select_dir_button = tk.Button(self.root, text="Select Directory", command=self.select_download_dir)
        self.select_dir_button.grid(row=1, column=0, padx=10, pady=10)

        # create label to display download directory
        self.dir_label = tk.Label(self.root, text="")
        self.dir_label.grid(row=1, column=1, padx=10, pady=10)

        # create drop-down menu for video resolution
        self.res_options = ["720p", "480p", "360p", "240p", "144p"]
        self.res_var = tk.StringVar(self.root)
        self.res_var.set(self.res_options[0])
        self.res_menu = tk.OptionMenu(self.root, self.res_var, *self.res_options)
        self.res_menu.grid(row=0, column=1, padx=10, pady=10)

        # create progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # create label for download status
        self.status_label = tk.Label(self.root, text="")
        self.status_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def download_video(self):
        # get video url from entry widget
        url = self.url_entry.get()

        # get video object from pytube library
        try:
            video = YouTube(url)
        except:
            self.status_label["text"] = "Error: Invalid URL"
            return

        # get selected video resolution from drop-down menu
        selected_res = self.res_var.get()
        stream = video.streams.filter(res=selected_res).first()

        # get download directory from label
        download_dir = self.dir_label["text"]

        # start download and show progress
        self.progress["value"] = 0
        self.progress["maximum"] = 100
        self.progress.start(10)
        self.status_label["text"] = "Downloading..."
        try:
            stream.download(download_dir)
        except:
            self.status_label["text"] = "Error: Download Failed"
            return
        self.progress.stop()
        self.progress["value"] = 100
        self.status_label["text"] = "Download Complete!"

    def select_download_dir(self):
        # open file dialog to select download directory
        download_dir = filedialog.askdirectory()

        # set label to display selected directory
        self.dir_label["text"] = download_dir

if __name__ == "__main__":
    # create main window
    root = tk.Tk()

    # create YouTube downloader object
    downloader = YoutubeDownloader(root)

    # run main loop
    root.mainloop()
