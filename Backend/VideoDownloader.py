from pytube import YouTube
from Error import DownloadError

class VideoDownloader:
    def __init__(self):
        self.video_link = ""
        self.file_path = ""

    def set_url(self, link):
        self.video_link = link

    def set_download_path(self, path):
        self.file_path = path

    def download_video(self):
        try:
            video = YouTube(self.video_link)
            mp3_name = f'{video.streams[0].title}.mp3'
            video.streams.filter(only_audio=True).first().download(output_path=self.file_path, filename=mp3_name)
            return self.format_download_info(video)
        except Exception as e:
            errorLink = 'regex_search: could not find match for (?:v=|\/)([0-9A-Za-z_-]{11}).*'
            errorConexion = '<urlopen error [Errno 11001] getaddrinfo failed>'
            if str(e) == errorLink:
                raise DownloadError("Ingrese una URL de video válida.")
            elif str(e) == errorConexion:
                raise DownloadError("No estás conectado a internet. Revisa tu conexión.")
            else:
                raise DownloadError(str(e))

    
    def format_download_info(self, video):
        duration = self.format_duration(video.length)
        return f"Download complete...\n\nTitle: {video.title} \nAuthor: {video.author} \nDuration: {duration}"

    def format_duration(self, duration):
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f'{minutes:02d}:{seconds:02d}'



    

        