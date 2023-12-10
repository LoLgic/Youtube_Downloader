import customtkinter as ctk
import tkinter as tk
from tkinter import Canvas, Menu, messagebox, PhotoImage, filedialog
from PIL import Image
import webbrowser

from Utils import Config
from Backend import VideoDownloader
from Error import DownloadError

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.config_var = Config()
        self.video_downloader = VideoDownloader()

        self.title("YouTube Downloader")
        self.iconbitmap(self.config_var.icon_image_path)
        self.resizable(False,False)

        self.create_menu()
        self.create_page()
       
    def create_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        helpMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Para más imformacíon", menu=helpMenu)
        helpMenu.add_command(label="Informacíon del autor", command=self.popup)
        menubar.add_command(label="Salir", command=self.destroy)
    
    def popup(self):
        messagebox.showinfo("Sobre la app", "Descarga videos de YouTube y los convierte a mp3.")
    
    def create_page(self):
        canvas = Canvas(self,
                        width=500,
                        height=800,
                        bg=self.config_var.color_bg)
        canvas.pack()

        self.logo_img = PhotoImage(file=self.config_var.logo_image_path)
        self.logo_img = self.logo_img.subsample(1, 1)
        canvas.create_image(250, 200, image=self.logo_img)

        title_label = ctk.CTkLabel(self,
                                   text="YouTube mp3\nDownloader",
                                   width=400,
                                   font=('Arial Rounded MT',35,'bold',),
                                   text_color=self.config_var.color_text,
                                   bg_color=self.config_var.color_bg
                                   )
        title_label.place(relx=0.5, rely=0.27, anchor=tk.CENTER)

        url_label = ctk.CTkLabel(self,
                                 text="Video Link",
                                 font=('Arial Rounded MT',14,'bold',),
                                 text_color=self.config_var.color_text,
                                 bg_color=self.config_var.color_bg
                                 )
        url_label.place(relx=0.25, rely=0.51, anchor=tk.CENTER)


        self.url_entry = ctk.CTkEntry(self,
                                      width=300,
                                      height=30,
                                      font=('Arial Rounded MT',14,),
                                      text_color=self.config_var.color_text,
                                      bg_color=self.config_var.color_bg,
                                      placeholder_text="Pegue el enlace de su video aquí"
                                      )
        self.url_entry.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        imgButton =  ctk.CTkImage(Image.open(self.config_var.download_img_path)) 
        download_button = ctk.CTkButton(self,
                                        text="Download",
                                        font=('Arial Rounded MT',20,'bold',),
                                        width=150,
                                        height=40,
                                        corner_radius=5,
                                        image=imgButton,
                                        text_color=self.config_var.color_text,
                                        bg_color=self.config_var.color_bg,
                                        fg_color=self.config_var.color_btn,
                                        hover_color=self.config_var.color_btnDark,
                                        command=self.btn_download
                                        )
        download_button.place(relx=0.5, rely=0.63, anchor=tk.CENTER)

        self.location_label = ctk.CTkLabel(self,
                                           text="",
                                           font=('Arial Rounded MT',14,),
                                           text_color=self.config_var.color_text,
                                           bg_color=self.config_var.color_bg)
        self.location_label.place(relx=0.5, rely=0.70, anchor=tk.CENTER)

        self.estado_label = ctk.CTkLabel(self,
                                         text="",
                                         font=('Arial Rounded MT',12,),
                                         justify="left",
                                         text_color=self.config_var.color_text,
                                         bg_color=self.config_var.color_bg   
                                         )
        self.estado_label.place(relx=0.5, rely=0.80, anchor=tk.CENTER)

        imgGithub = ctk.CTkImage(Image.open(self.config_var.github_image_path))
        github_button = ctk.CTkButton(self,
                                      text="",
                                      width=0,
                                      height=0,
                                      image=imgGithub,
                                      fg_color=self.config_var.color_bg,
                                      hover_color=self.config_var.color_bg,
                                      command=self.open_link
                                      )
        github_button.place(relx=0.1, rely=0.95, anchor=tk.CENTER)

        github_label = ctk.CTkLabel(self,
                                    text="GitHub",
                                    font=('Arial Rounded MT',14,'bold',),
                                    text_color=self.config_var.color_text,
                                    bg_color=self.config_var.color_bg)
        github_label.place(relx=0.2, rely=0.95, anchor=tk.CENTER)

        creator_label = ctk.CTkLabel(self,
                                     text="Create by Mario Petro",
                                     font=('Arial Rounded MT',10,'bold',),
                                     text_color=self.config_var.color_text,
                                     bg_color=self.config_var.color_bg)
        creator_label.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

    def open_link(self):
        webbrowser.open(self.config_var.github_link)


    def btn_download(self):
        link = self.url_entry.get()
        if link:
            path = filedialog.askdirectory()
            self.location_label.configure(text=path)
            download_path = self.location_label.cget("text")
            if download_path:
                self.estado_label.configure(text="Descargando...")
                self.update()
                self.video_downloader.set_url(link)
                self.video_downloader.set_download_path(download_path)
                try:
                    status = self.video_downloader.download_video()
                    self.estado_label.configure(text=status)
                except DownloadError as e:
                    messagebox.showerror("Download Error", str(e))
                    self.estado_label.configure(text="")
                
                




            
       


                                   