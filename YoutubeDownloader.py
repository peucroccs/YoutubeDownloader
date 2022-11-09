from tkinter import *
from pytube import YouTube
import pytube.request
import threading

pytube.request.default_range_size = 6437184

class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("YouTube Downloader")
        self.root.geometry("800x600")
        self.interface(self.root)

    def interface(self, master):
        self.instrucao1 = Label(master, text="Insira um link do YouTube", font=("Arial", "18", "bold"))
        self.instrucao1.place(x=230, y=140)

        self.name_label = Label(master, text="Nome do Arquivo: ", font=("Arial", "10", 'bold'))
        self.name_label.place(x=200, y=200)

        self.name_var = StringVar()
        self.name_input = Entry(master, textvariable=self.name_var, width=30, font=("Arial", "10"))
        self.name_input.place(x=330, y=200)

        self.link_label = Label(master, text="Link: ", font=("Arial", "10", 'bold'))
        self.link_label.place(x=200, y=230)

        self.link_var = StringVar()
        self.link_input = Entry(master, textvariable=self.link_var, width=30, font=("Arial", "10"))
        self.link_input.place(x=330, y=230)

        self.download = Button(master, text="Download", width=10, font=("Calibri", "14"))
        self.download["command"] = threading.Thread(target=self.download_video).start
        self.download.place(x=430, y=270)

        self.exit = Button(master, text='X', width=10, bg='red', font=('Calibri', '14'))
        self.exit['command'] = self.quit
        self.exit.place(x=680, y=20)

    def progress_bar(self, stream, _chunk, bytes_remaining):
        current = ((stream.filesize - bytes_remaining) / stream.filesize)
        percent = '{0:.1f}'.format(current*100)
        progress = int(37 * current)
        status = '█' * progress + '-' * (37 - progress)
        self.progress_label = Label(self.root, text='|{bar}| {percent}%\r'.format(bar=status, percent=percent),
                               font=('Arial', '10'))
        self.progress_label.place(x=200, y=310)
        if stream.filesize - bytes_remaining == stream.filesize:
            self.complete_label = Label(self.root, text='Download Completo | {:.2f} MB baixados'.format(stream.filesize*0.000001),
            font=('Arial', '10'))
            self.complete_label.place(x=200, y=330)

    def download_video(self):
        link = self.link_var.get()
        yt = YouTube(link)
        yt.register_on_progress_callback(self.progress_bar)
        video = yt.streams.filter(file_extension='mp4').get_highest_resolution()
        video.download(filename=self.name_var.get() + self.get_extension(video.default_filename))

    def get_extension(self, file):
        dot = file.rfind('.')
        extension = file[dot:]
        return extension

    def execute(self):
        self.root.mainloop()

    def quit(self):
        self.root.quit()


if __name__ == '__main__':
    App = App()
    App.execute()
